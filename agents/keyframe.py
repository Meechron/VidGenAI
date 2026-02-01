"""Keyframe agent that generates images from detailed prompts."""

import os
import sys
import time

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.base import BaseAgent
from models.replicate_client import ReplicateClient


class KeyframeAgent(BaseAgent):
    """Generates images from prompts using Replicate's Flux model."""

    def __init__(self):
        super().__init__("Keyframe")
        self.replicate = ReplicateClient()

    def run(self, scene_data, output_folder):
        """Generate keyframe images from scene prompts."""
        self.log(f"Generating {len(scene_data['keyframes'])} keyframes")

        os.makedirs(output_folder, exist_ok=True)
        generated_images = []

        for i, keyframe in enumerate(scene_data['keyframes']):
            keyframe_id = keyframe['keyframe_id']
            prompt = keyframe['prompt']

            self.log(f"[{i+1}/{len(scene_data['keyframes'])}] {keyframe_id}")

            try:
                image_url = self.replicate.generate_image(
                    prompt=prompt,
                    aspect_ratio="16:9"
                )

                save_path = os.path.join(output_folder, f"{keyframe_id}.png")
                self.replicate.download_image(image_url, save_path)

                generated_images.append(save_path)

                if i < len(scene_data['keyframes']) - 1:
                    time.sleep(12)

            except Exception as e:
                self.log(f"ERROR: {e}")

        self.log(f"Done - {len(generated_images)} images generated")
        return generated_images
