import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from .model_loader import get_model_instance

app = FastAPI(title="AI System - FastAPI")

# Create a small thread pool for blocking model.generate calls
_executor = ThreadPoolExecutor(max_workers=int(os.environ.get("INFERENCE_THREADS", "4")))

# Instantiate loader but keep actual heavy load lazy
MODEL_ID = os.environ.get("MODEL_ID", "gpt2")
USE_ONNX = os.environ.get("USE_ONNX", "false").lower() == "true"
model = get_model_instance(MODEL_ID, use_onnx=USE_ONNX)


class PredictRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 128


@app.on_event("startup")
async def startup_event():
    # optional: pre-load model into memory to avoid first-request latency
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(_executor, model.load)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(req: PredictRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt required")
    loop = asyncio.get_running_loop()
    # run blocking inference in threadpool to keep event loop responsive
    result = await loop.run_in_executor(_executor, model.generate, req.prompt, req.max_new_tokens)
    return {"generated_text": result}
