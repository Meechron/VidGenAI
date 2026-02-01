"""Wrapper for the Claude API with text and vision capabilities."""

import os
import base64
import json
from dotenv import load_dotenv
import anthropic

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH, override=True)


class ClaudeClient:
    """Wrapper for the Claude API with support for text and vision."""

    def __init__(self, model="claude-sonnet-4-20250514"):
        """Initialize Claude client with API key from environment."""
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Make sure you have a .env file with your API key."
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def send_message(self, prompt, max_tokens=4096):
        """Send a text prompt and return Claude's response."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def send_message_with_image(self, prompt, image_path, max_tokens=4096):
        """Send a prompt with an image and return Claude's response."""
        with open(image_path, "rb") as f:
            image_data = f.read()

        image_base64 = base64.standard_b64encode(image_data).decode("utf-8")

        extension = os.path.splitext(image_path)[1].lower()
        media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        media_type = media_types.get(extension, "image/png")

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_base64
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            }]
        )

        return message.content[0].text

    def send_message_with_images(self, prompt, image_paths, max_tokens=4096):
        """Send a prompt with multiple images and return Claude's response."""
        content = []

        for image_path in image_paths:
            with open(image_path, "rb") as f:
                image_data = f.read()

            image_base64 = base64.standard_b64encode(image_data).decode("utf-8")

            extension = os.path.splitext(image_path)[1].lower()
            media_types = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }
            media_type = media_types.get(extension, "image/png")

            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_base64
                }
            })

        content.append({"type": "text", "text": prompt})

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": content}]
        )

        return message.content[0].text

    def send_structured(self, prompt, max_tokens=4096):
        """Send a prompt and parse the JSON response."""
        text_response = self.send_message(prompt, max_tokens)
        text = text_response.strip()

        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON from Claude's response.\n"
                f"Error: {e}\n"
                f"Response: {text_response[:500]}..."
            )
