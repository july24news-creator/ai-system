# ai-system (example)

This repository contains a minimal FastAPI server and a lazy model loader to run a language model with faster startup and lower first-request latency.

Quick start (local)
1. Create a virtualenv and install requirements:
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt

2. Set MODEL_ID to a Hugging Face model or local path:
   export MODEL_ID="gpt2"  # replace with your model

3. Run:
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2

Performance & faster loading tips
- Use ONNX / TorchScript export for faster cold-start and inference with onnxruntime.
- Quantize the model (8-bit, 4-bit) using tools like bitsandbytes or ONNX quantization.
- Pre-warm the model at startup (startup event already calls model.load()).
- Use lazy imports and avoid importing heavy ML libraries at module import time.
- Use Redis or in-memory caches for repeated requests.
- For production, use a process manager (gunicorn + uvicorn workers) behind a load balancer.

Deployment notes
- The provided Dockerfile is a minimal CPU image. For GPU support, use an NVIDIA CUDA base image and install the appropriate CUDA toolkit and drivers. Ensure your container runtime supports GPUs (nvidia-container-runtime / NVIDIA Container Toolkit).
- If you wish, I can add a model-puller to fetch large model artifacts from S3/MinIO at container startup to avoid baking models into images.


---

Please note: If you want extra files (CI, Docker Compose, export-to-ONNX script, or a benchmarking script), tell me which one and I'll add it. The Dockerfile is included as requested.
