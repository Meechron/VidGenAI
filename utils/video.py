"""Video assembly utilities using OpenCV."""

import os
import cv2
import glob


def images_to_video(image_paths, output_path, fps=24, duration_per_image=1.0):
    """Create a video from a list of images, showing each for specified duration."""
    if not image_paths:
        raise ValueError("No images provided!")

    output_folder = os.path.dirname(output_path)
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    first_image = cv2.imread(image_paths[0])
    if first_image is None:
        raise ValueError(f"Could not read image: {image_paths[0]}")

    height, width = first_image.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    frames_per_image = int(fps * duration_per_image)

    for i, image_path in enumerate(image_paths):
        print(f"  Adding image {i+1}/{len(image_paths)}: {os.path.basename(image_path)}")

        image = cv2.imread(image_path)
        if image is None:
            print(f"  WARNING: Could not read {image_path}, skipping")
            continue

        if image.shape[:2] != (height, width):
            image = cv2.resize(image, (width, height))

        for _ in range(frames_per_image):
            video_writer.write(image)

    video_writer.release()
    return output_path


def frames_to_video(frames_folder, output_path, fps=24):
    """Create a video from a folder of sequential frames."""
    pattern = os.path.join(frames_folder, "*.png")
    frame_paths = sorted(glob.glob(pattern))

    if not frame_paths:
        raise ValueError(f"No PNG files found in {frames_folder}")

    print(f"  Found {len(frame_paths)} frames")

    return images_to_video(
        frame_paths,
        output_path,
        fps=fps,
        duration_per_image=1.0/fps
    )
