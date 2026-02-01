"""File I/O utilities for saving and loading project data."""

import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


def save_json(data, path):
    """Save dictionary as JSON file."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_json(path):
    """Load JSON file and return as dictionary."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_project_folder(project_id):
    """Create folder structure for a video project."""
    project_folder = os.path.join(OUTPUT_DIR, project_id)

    os.makedirs(project_folder, exist_ok=True)
    os.makedirs(os.path.join(project_folder, "3_keyframes"), exist_ok=True)
    os.makedirs(os.path.join(project_folder, "5_interpolated"), exist_ok=True)

    return project_folder


def get_project_path(project_id, filename):
    """Get full path for a file within a project."""
    return os.path.join(OUTPUT_DIR, project_id, filename)
