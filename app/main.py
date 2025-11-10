import os
import asyncio
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from .model_loader import get_model_instance
from .pipeline.manager import run_ingest_job, IngestJob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-system")

app = FastAPI(title="AI System - Pipeline-enabled")

# CORS settings (configure via env)
_allow_origins = os.environ.get("ALLOW_ORIGINS", "*")
if _allow_origins.strip() == "":
    origins = ["*"]
else:
    origins = [o.strip() for o in _allow_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Billing guard (default: disabled)
if os.environ.get("DISABLE_BILLING", "true").lower() in ("1", "true", "yes"):
    logger.info("Billing integrations are disabled by configuration (DISABLE_BILLING=true).")
    BILLING_ENABLED = False
else:
    BILLING_ENABLED = True

# Small threadpool for blocking tasks
_executor = ThreadPoolExecutor(max_workers=int(os.environ.get("INFERENCE_THREADS", "4")))

MODEL_ID = os.environ.get("MODEL_ID", "gpt2")
USE_ONNX = os.environ.get("USE_ONNX", "false").lower() == "true"
model = get_model_instance(MODEL_ID, use_onnx=USE_ONNX)

class PredictRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 128

class IngestRequest(BaseModel):
    source_type: str                # e.g. "rss", "api", "web"
    source: str                     # URL or identifier
    options: Optional[dict] = None  # optional configuration

@app.on_event("startup")
async def startup_event():
    # Optionally preload the model to reduce first-request latency
    if os.environ.get("PRELOAD_MODEL", "true").lower() == "true":
        logger.info("Preloading model...")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(_executor, model.load)
        logger.info("Model preloaded.")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/model/status")
async def model_status():
    try:
        status = {
            "model_id": model.model_name_or_path,
            "device": model.device,
            "loaded": model.model is not None and model.tokenizer is not None,
        }
        return status
    except Exception as e:
        logger.exception("Error in /model/status")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/model/reload")
async def model_reload(background_tasks: BackgroundTasks):
    """
    Trigger model reload in background. Useful after pulling new artifacts.
    """
    def _reload():
        try:
            logger.info("Reloading model...")
            model.model = None
            model.tokenizer = None
            model.load()
            logger.info("Reload complete.")
        except Exception:
            logger.exception("Model reload failed.")
    background_tasks.add_task(_reload)
    return {"status": "reload_started"}

@app.post("/predict")
async def predict(req: PredictRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt required")
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(_executor, model.generate, req.prompt, req.max_new_tokens)
        return {"generated_text": result}
    except Exception as e:
        logger.exception("Inference error")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest(req: IngestRequest, background_tasks: BackgroundTasks, request: Request):
    """
    Accepts ingestion jobs (RSS / API / web scrape / webhook payload).
    Returns a job ID and runs ingestion in background.
    """
    job = IngestJob(source_type=req.source_type, source=req.source, options=req.options or {}, requested_by=request.client.host)
    # run ingestion in background
    background_tasks.add_task(run_ingest_job, job)
    return {"status": "ingest_started", "job_id": job.job_id}

@app.post("/webhook")
async def webhook(payload: dict, background_tasks: BackgroundTasks, request: Request):
    """
    Generic webhook endpoint: accept JSON payloads and forward into pipeline as a 'web' ingestion.
    """
    source = request.url.path  # or use a configured name
    job = IngestJob(source_type="web", source=source, options={"payload": payload}, requested_by=request.client.host)
    background_tasks.add_task(run_ingest_job, job)
    return {"status": "webhook_received", "job_id": job.job_id}
