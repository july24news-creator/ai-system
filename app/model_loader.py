import os
import threading
from typing import Optional

import torch

# Try importing heavy ML libs lazily in functions to keep import time short
from transformers import AutoModelForCausalLM, AutoTokenizer

_lock = threading.Lock()
_instance = None


class ModelWrapper:
    def __init__(self, model_name_or_path: str, device: Optional[str] = None, use_onnx: bool = False):
        self.model_name_or_path = model_name_or_path
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.use_onnx = use_onnx
        self.tokenizer = None
        self.model = None

    def load(self):
        # lazy load tokenizer + model
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, padding_side="left", use_fast=True)

        # If you exported an ONNX model and want to use onnxruntime, set use_onnx=True and implement ORT session
        if self.use_onnx:
            try:
                import onnxruntime as ort
                onnx_path = os.environ.get("ONNX_MODEL_PATH", self.model_name_or_path)
                self.model = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
            except Exception:
                # fallback to transformers
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path).to(self.device)
        else:
            # Try to reduce memory: load in 8-bit if available (requires bitsandbytes, optional)
            try:
                # from transformers import BitsAndBytesConfig  # optional
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path, torch_dtype=torch.float16 if self.device.startswith("cuda") else torch.float32)
                self.model.to(self.device)
            except Exception:
                # fallback simple load
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path)
                self.model.to(self.device)

    def generate(self, prompt: str, max_new_tokens: int = 128, **gen_kwargs):
        if self.model is None or self.tokenizer is None:
            self.load()

        # If onnx runtime: run through ORT session; else use model.generate
        if self.use_onnx and hasattr(self.model, "run"):
            # placeholder: implement ONNX execution mapping inputs -> outputs
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
            # convert to numpy and call session.run; omitted for brevity
            raise NotImplementedError("ONNX path: implement ORT run logic for your model")
        else:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, **gen_kwargs)
            return self.tokenizer.decode(out[0], skip_special_tokens=True)


def get_model_instance(model_name_or_path: str = None, device: Optional[str] = None, use_onnx: bool = False) -> ModelWrapper:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                model_name_or_path = model_name_or_path or os.environ.get("MODEL_ID", "gpt2")
                _instance = ModelWrapper(model_name_or_path, device=device, use_onnx=use_onnx)
    return _instance
