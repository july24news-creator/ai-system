import os
import uuid
import logging
import asyncio
from dataclasses import dataclass
from typing import Dict, Any

from .rss_fetcher import fetch_rss_items

logger = logging.getLogger("ai-system.pipeline")

@dataclass
class IngestJob:
    source_type: str
    source: str
    options: Dict[str, Any]
    requested_by: str = "unknown"
    job_id: str = None

    def __post_init__(self):
        if not self.job_id:
            self.job_id = uuid.uuid4().hex

async def _process_rss(job: IngestJob):
    logger.info("Processing RSS job %s -> %s", job.job_id, job.source)
    items = await fetch_rss_items(job.source)
    # Here you would transform items, store into DB/MinIO, send to embedding/indexing, or push to model
    logger.info("Fetched %d items from %s", len(items), job.source)
    # for demo: just log titles
    for it in items[:5]:
        logger.info("Item: %s", it.get("title"))

async def _process_api(job: IngestJob):
    logger.info("Processing API job %s -> %s", job.job_id, job.source)
    # extend with custom API fetching logic (rate limiting, auth)
    await asyncio.sleep(0.1)
    logger.info("API ingest complete for %s", job.source)

async def _process_web(job: IngestJob):
    logger.info("Processing Webhook job %s -> %s", job.job_id, job.source)
    payload = job.options.get("payload")
    # store or forward payload
    logger.info("Payload keys: %s", list(payload.keys()) if isinstance(payload, dict) else "non-dict")

def _dispatch_task(job: IngestJob):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if job.source_type == "rss":
            loop.run_until_complete(_process_rss(job))
        elif job.source_type == "api":
            loop.run_until_complete(_process_api(job))
        else:
            loop.run_until_complete(_process_web(job))
    finally:
        loop.close()

def run_ingest_job(job: IngestJob):
    """
    Entry point for background tasks. Can be run from FastAPI BackgroundTasks or worker processes.
    """
    logger.info("Starting ingest job %s type=%s", job.job_id, job.source_type)
    try:
        _dispatch_task(job)
        logger.info("Ingest job %s finished", job.job_id)
    except Exception:
        logger.exception("Ingest job %s failed", job.job_id)
