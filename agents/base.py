"""Base agent class for the video generation pipeline."""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.claude_client import ClaudeClient


class BaseAgent:
    """Base class for all agents in the video generation pipeline."""

    def __init__(self, name):
        """Initialize the agent with a name and Claude client."""
        self.name = name
        self.claude = ClaudeClient()
        self.log("Initialized")

    def log(self, message):
        """Print a message prefixed with the agent's name."""
        print(f"[{self.name}] {message}")

    def run(self, input_data):
        """Execute the agent's main task. Must be overridden by subclasses."""
        raise NotImplementedError(
            f"{self.name} agent must implement the run() method!"
        )
