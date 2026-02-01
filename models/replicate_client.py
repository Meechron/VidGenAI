"""Wrapper for the Replicate API to handle image generation and frame interpolation."""

import os
import requests
from dotenv import load_dotenv
import replicate

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH, override=True)


class ReplicateClient:
    """Wrapper for the Replicate API supporting Flux image generation and FILM interpolation."""

    def __init__(self):
        """Initialize Replicate client with API token from environment."""
        token = os.getenv("REPLICATE_API_TOKEN")
        if not token:
            raise ValueError(
                "REPLICATE_API_TOKEN not found. "
                "Make sure you have a .env file with your API token."
            )

    def generate_image(self, prompt, aspect_ratio="16:9"):
        """Generate an image from a text prompt using Flux Schnell."""
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "output_format": "png",
                "output_quality": 90,
                "num_outputs": 1,
                "go_fast": True
            }
        )

        if output and len(output) > 0:
            return output[0]
        else:
            raise ValueError("No image was generated")

    def download_image(self, url, save_path):
        """Download an image from URL and save to disk."""
        folder = os.path.dirname(save_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        response = requests.get(url)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            f.write(response.content)

        return save_path

    def interpolate_frames(self, image1_path, image2_path):
        """Generate intermediate frames between two images using FILM model."""
        output = replicate.run(
            "google-research/frame-interpolation",
            input={
                "frame1": open(image1_path, "rb"),
                "frame2": open(image2_path, "rb"),
                "times_to_interpolate": 4
            }
        )

        if output:
            if isinstance(output, list):
                return output[0] if len(output) > 0 else None
            return output
        else:
            raise ValueError("No interpolated frames were generated")
