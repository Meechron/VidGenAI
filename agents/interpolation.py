"""Interpolation agent that generates smooth transitions between keyframes using FILM."""

import os
import sys
import time

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.base import BaseAgent
from models.replicate_client import ReplicateClient
from PIL import Image


class InterpolationAgent(BaseAgent):
    """Creates smooth motion between keyframes using the FILM model."""

    def __init__(self):
        super().__init__("Interpolation")
        self.replicate = ReplicateClient()

    def run(self, keyframe_paths, output_folder):
        """Generate smooth frames between keyframes using FILM model."""
        self.log(f"Interpolating {len(keyframe_paths)} keyframes")

        os.makedirs(output_folder, exist_ok=True)
        all_frames = []
        frame_counter = 0

        for i in range(len(keyframe_paths) - 1):
            frame1_path = keyframe_paths[i]
            frame2_path = keyframe_paths[i + 1]

            self.log(f"[{i+1}/{len(keyframe_paths)-1}] {os.path.basename(frame1_path)} -> {os.path.basename(frame2_path)}")

            time.sleep(12)

            try:
                if i == 0:
                    frame_counter += 1
                    dest_path = os.path.join(output_folder, f"frame_{frame_counter:04d}.png")
                    self._copy_image(frame1_path, dest_path)
                    all_frames.append(dest_path)

                video_url = self.replicate.interpolate_frames(frame1_path, frame2_path)

                extracted = self._extract_frames_from_video(
                    video_url,
                    output_folder,
                    frame_counter + 1
                )

                for path in extracted:
                    frame_counter += 1
                    all_frames.append(path)

                frame_counter += 1
                dest_path = os.path.join(output_folder, f"frame_{frame_counter:04d}.png")
                self._copy_image(frame2_path, dest_path)
                all_frames.append(dest_path)

            except Exception as e:
                self.log(f"ERROR: {e}")
                if i == 0:
                    frame_counter += 1
                    dest_path = os.path.join(output_folder, f"frame_{frame_counter:04d}.png")
                    self._copy_image(frame1_path, dest_path)
                    all_frames.append(dest_path)

                frame_counter += 1
                dest_path = os.path.join(output_folder, f"frame_{frame_counter:04d}.png")
                self._copy_image(frame2_path, dest_path)
                all_frames.append(dest_path)

        self.log(f"Done - {len(all_frames)} total frames")
        return all_frames

    def _copy_image(self, src_path, dest_path):
        """Copy an image file to a new location."""
        img = Image.open(src_path)
        img.save(dest_path)

    def _extract_frames_from_video(self, video_url, output_folder, start_num):
        """Download video and extract frames."""
        import cv2

        temp_video = os.path.join(output_folder, "temp_interpolated.mp4")
        self.replicate.download_image(video_url, temp_video)

        cap = cv2.VideoCapture(temp_video)
        frames = []
        frame_num = start_num

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            dest_path = os.path.join(output_folder, f"frame_{frame_num:04d}.png")
            cv2.imwrite(dest_path, frame)
            frames.append(dest_path)
            frame_num += 1

        cap.release()

        try:
            os.remove(temp_video)
        except:
            pass

        return frames
