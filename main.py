"""VidGen entry point - CLI interface for video generation."""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from orchestrator import Orchestrator


def print_banner():
    """Print a nice welcome banner."""
    print()
    print("=" * 60)
    print("  __     ___     _  ____            ")
    print("  \\ \\   / (_) __| |/ ___| ___ _ __  ")
    print("   \\ \\ / /| |/ _` | |  _ / _ \\ '_ \\ ")
    print("    \\ V / | | (_| | |_| |  __/ | | |")
    print("     \\_/  |_|\\__,_|\\____|\\___|_| |_|")
    print()
    print("  AI Video Generator - Text to Video")
    print("=" * 60)
    print()


def get_prompt_from_user():
    """Interactively get video prompt from user."""
    print("Enter a description of the video you want to create:")
    print("  Examples: 'A knight fights a dragon', 'A cat playing with yarn'\n")

    while True:
        prompt = input("Prompt: ").strip()

        if not prompt:
            print("Please enter a prompt (or 'quit' to exit)")
            continue

        if prompt.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            sys.exit(0)

        print(f"\nGenerating: \"{prompt}\"")
        confirm = input("Continue? (y/n): ").strip().lower()

        if confirm in ['y', 'yes', '']:
            return prompt
        else:
            print()


def main():
    """Main entry point."""
    print_banner()

    args = sys.argv[1:]
    if args:
        prompt = " ".join(args)
        print(f"Prompt: \"{prompt}\"\n")
    else:
        prompt = get_prompt_from_user()

    try:
        orchestrator = Orchestrator()
        video_path = orchestrator.run(prompt)

        print("\n" + "=" * 60)
        print(f"SUCCESS! Video ready: {video_path}")
        print("=" * 60 + "\n")

        return 0

    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        return 1

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("  - Check API keys in .env")
        print("  - Verify internet connection")
        print("  - Ensure Replicate account has credit\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
