"""Merge a distil labs LoRA adapter into its base model, so llama.cpp can convert it to GGUF.

Usage: .venv/bin/python merge.py <model-dir> <out-dir>
<model-dir> is the extracted `distil slm download` folder (it holds model-adapter/ and config.yaml).
"""
import shutil
import sys
from pathlib import Path

import json

import torch
from peft import PeftModel
from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForImageTextToText, AutoTokenizer

model_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
adapter = model_dir / "model-adapter"
base_name = json.load(open(adapter / "adapter_config.json"))["base_model_name_or_path"]
arch = AutoConfig.from_pretrained(base_name).architectures[0]
print("base model:", base_name, arch)

# Qwen3.5 checkpoints are vision-language models (Qwen3_5ForConditionalGeneration) and the adapter targets
# model.language_model.*, so load the same class the platform trained, not the text-only one.
loader = AutoModelForImageTextToText if arch.endswith("ForConditionalGeneration") else AutoModelForCausalLM
base = loader.from_pretrained(base_name, dtype=torch.bfloat16)
merged = PeftModel.from_pretrained(base, adapter).merge_and_unload()
merged.save_pretrained(out, safe_serialization=True)
AutoTokenizer.from_pretrained(adapter if (adapter / "tokenizer_config.json").exists() else base_name).save_pretrained(out)
if (adapter / "chat_template.jinja").exists():  # the template the model was trained with
    shutil.copy(adapter / "chat_template.jinja", out / "chat_template.jinja")
print("merged model written to", out)
