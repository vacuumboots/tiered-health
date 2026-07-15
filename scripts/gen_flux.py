#!/usr/bin/env python3
"""Generate a medical illustration using FLUX.1 Dev on Apple Silicon MPS."""
import torch
from diffusers import FluxPipeline
from huggingface_hub import HfFolder
import sys, os

PROMPT = sys.argv[1] if len(sys.argv) > 1 else (
    "Clean medical textbook illustration of lateral ankle sprain anatomy. "
    "Shows the fibula bone and talus bone with three lateral ligaments labeled: "
    "anterior talofibular ligament (ATFL), calcaneofibular ligament (CFL), "
    "posterior talofibular ligament (PTFL). "
    "White background, precise thin black line art, anatomical accuracy, "
    "Netter's anatomy atlas style, no shading, no color fill, "
    "clear readable labels with leader lines. Educational medical diagram."
)
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "flux_test.png"
STEPS = int(sys.argv[3]) if len(sys.argv) > 3 else 28
MODEL = "black-forest-labs/FLUX.1-dev"

# Load auth token from cache or env
token = os.environ.get("HF_TOKEN") or HfFolder.get_token()
if not token:
    print("ERROR: No HF token found. Run: huggingface-cli login")
    sys.exit(1)

print(f"Model: {MODEL}")
print(f"Prompt: {PROMPT}")
print(f"Steps: {STEPS}")
print(f"Output: {OUTPUT}")
print()

print("Loading model (first time downloads ~23GB, subsequent loads are instant)...")
pipe = FluxPipeline.from_pretrained(
    MODEL,
    torch_dtype=torch.float16,
    token=token,
).to("mps")

print(f"Generating ({STEPS} steps on MPS)...")
image = pipe(
    PROMPT,
    guidance_scale=3.5,
    num_inference_steps=STEPS,
    width=1024,
    height=768,
    generator=torch.Generator("mps").manual_seed(42),
).images[0]

image.save(OUTPUT)
print(f"Saved: {OUTPUT}")
print(f"Size: {image.size}")
