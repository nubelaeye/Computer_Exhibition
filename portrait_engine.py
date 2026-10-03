import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load .env from the APEX AI project folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


class PortraitEngine:

    MODEL = "black-forest-labs/FLUX.2-klein-9B"

    PROMPT = """
    Transform this portrait into a polished artistic animated illustration.

    Preserve the person's overall facial appearance, hairstyle, clothing,
    pose and composition as closely as possible.

    Use expressive clean linework, soft colors, appealing animated-film
    aesthetics, natural lighting and a refined digital illustration finish.

    Keep the person recognizable and do not add extra people or objects.
    """

    def __init__(self):

        # Get the variable named HF_TOKEN
        token = os.getenv("HF_TOKEN")

        if not token:
            raise RuntimeError(
                "HF_TOKEN is not available in the environment."
            )

        self.client = InferenceClient(
            provider="fal-ai",
            api_key=token
        )

    def generate(self, input_path, output_path):

        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            
            raise FileNotFoundError(
                f"Input image not found: {input_path}"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        print("[APEX AI] Loading portrait...")

        with open(input_path, "rb") as image_file:
            image_data = image_file.read()

        print("[APEX AI] Sending image to model...")
        print("[APEX AI] Generating artistic portrait...")

        result = self.client.image_to_image(
            image_data,
            prompt=self.PROMPT,
            model=self.MODEL
        )

        result.save(output_path)

        print(
            f"[APEX AI] Portrait saved → {output_path}"
        )

        return output_path
