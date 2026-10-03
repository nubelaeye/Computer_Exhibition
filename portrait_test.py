import os
from pathlib import Path

from huggingface_hub import InferenceClient


# ============================================================
# SETTINGS
# ============================================================

MODEL = "black-forest-labs/FLUX.2-klein-9B"

INPUT_IMAGE = Path("output/test_portrait.jpg")
OUTPUT_IMAGE = Path("output/apex_ai_portrait.png")


# ============================================================
# CHECK TOKEN
# ============================================================

token = os.getenv("HF_TOKEN")

if not token:
    raise RuntimeError(
        "HF_TOKEN was not found.\n"
        "Set it in PowerShell before running this program."
    )


# ============================================================
# CHECK INPUT
# ============================================================

if not INPUT_IMAGE.exists():
    raise FileNotFoundError(
        f"Input image not found: {INPUT_IMAGE}"
    )


# ============================================================
# CREATE CLIENT
# ============================================================

client = InferenceClient(
    provider="fal-ai",
    api_key=token
)


# ============================================================
# PROMPT
# ============================================================

prompt = """
Transform this portrait into a high-quality hand-drawn
animated illustration.

Preserve the person's identity, facial structure, hairstyle,
pose, clothing and overall composition.

Use clean expressive line art, soft colors, appealing
animated-film aesthetics, natural lighting and a polished
digital illustration appearance.

Do not add extra people or objects.
"""


# ============================================================
# SEND IMAGE TO AI
# ============================================================

print("🚀 APEX AI Portrait Engine")
print("📸 Loading image...")

with open(INPUT_IMAGE, "rb") as image_file:

    input_image = image_file.read()

print("☁️ Sending image to AI...")
print("🧠 Generating portrait...")


result = client.image_to_image(
    input_image,
    prompt=prompt,
    model=MODEL
)

# ============================================================
# SAVE RESULT
# ============================================================

result.save(
    OUTPUT_IMAGE
)

print()
print("✅ Portrait generated!")
print(f"📁 Saved to: {OUTPUT_IMAGE}")
