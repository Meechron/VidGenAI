"""Orchestrator that coordinates all agents to generate videos from text prompts."""

import os
import sys
import glob
import re

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.director import DirectorAgent
from agents.scene import SceneAgent
from agents.keyframe import KeyframeAgent
from agents.interpolation import InterpolationAgent
from utils.file_io import save_json, load_json, create_project_folder, get_project_path
from utils.video import images_to_video, frames_to_video


class Orchestrator:
    """Coordinates all agents to generate videos from text prompts."""

    def __init__(self):
        """Initialize all agents."""
        print("\n" + "=" * 60)
        print("VIDGEN - AI Video Generator")
        print("=" * 60 + "\n")

        self.director = DirectorAgent()
        self.scene = SceneAgent()
        self.keyframe = KeyframeAgent()
        self.interpolation = InterpolationAgent()

    def run(self, user_prompt):
        """Generate a video from a text prompt."""
        project_id = self._create_project_id(user_prompt)

        print(f"\nProject: {project_id}")
        print(f"Prompt: {user_prompt}")
        print("=" * 60 + "\n")

        project_folder = create_project_folder(project_id)

        print("STEP 1: Planning shots...")
        shot_plan = self.director.run(user_prompt)
        director_path = get_project_path(project_id, "1_director.json")
        save_json(shot_plan, director_path)

        print("\nSTEP 2: Creating detailed prompts...")
        scene_data = self.scene.run(shot_plan)
        scene_path = get_project_path(project_id, "2_scene.json")
        save_json(scene_data, scene_path)

        print("\nSTEP 3: Generating images...")
        keyframes_folder = get_project_path(project_id, "3_keyframes")
        generated_images = self.keyframe.run(scene_data, keyframes_folder)
        keyframe_paths = sorted(glob.glob(os.path.join(keyframes_folder, "*.png")))

        print("\nSTEP 4: Creating smooth transitions...")
        interpolated_folder = get_project_path(project_id, "4_interpolated")
        all_frames = self.interpolation.run(keyframe_paths, interpolated_folder)

        print("\nSTEP 5: Assembling video...")
        video_path = get_project_path(project_id, "final.mp4")
        frames_to_video(interpolated_folder, video_path, fps=24)

        video_frames = sorted(glob.glob(os.path.join(interpolated_folder, "*.png")))

        print("\n" + "=" * 60)
        print("VIDEO GENERATION COMPLETE!")
        print("=" * 60)
        print(f"\nOutput: {video_path}")
        print(f"Keyframes: {len(keyframe_paths)} | Total frames: {len(video_frames)}")

        return video_path

    def _create_project_id(self, prompt):
        """Create a safe folder name from the prompt with timestamp."""
        import time

        short = prompt[:30].lower()
        safe = re.sub(r'[^a-z0-9]+', '_', short).strip('_')
        timestamp = int(time.time())

        return f"{safe}_{timestamp}"


if __name__ == "__main__":
    orchestrator = Orchestrator()
    test_prompt = "A cat playing with a ball of yarn"
    video_path = orchestrator.run(test_prompt)
    print(f"\nTest complete! Video at: {video_path}")
