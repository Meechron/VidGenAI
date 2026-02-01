# VidGen

AI-powered text-to-video generator that creates short videos from text descriptions using Claude and Replicate.

## Features

- **Text-to-Video**: Convert natural language descriptions into videos
- **AI-Powered Pipeline**: Uses Claude for scene planning and Flux for image generation
- **Smooth Animations**: FILM model for frame interpolation (24fps output)
- **Automated Workflow**: Five-step pipeline from prompt to finished video

## Examples

```bash
python main.py "A knight fights a dragon in front of a burning castle"
python main.py "A cat playing with a ball of yarn in a sunny room"
python main.py "A rocket launching into space at sunset"
```

## Installation

### Prerequisites

- Python 3.8+
- [Anthropic API key](https://console.anthropic.com/)
- [Replicate API token](https://replicate.com/account/api-tokens)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/VidGen.git
cd VidGen
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Usage

### Interactive Mode
```bash
python main.py
```

### Command Line
```bash
python main.py "Your video description here"
```

### Output

Generated videos are saved in `output/{project_id}/final.mp4`

Each project folder contains:
- `1_director.json` - Shot plan
- `2_scene.json` - Detailed prompts
- `3_keyframes/` - Generated images
- `4_interpolated/` - Interpolated frames
- `final.mp4` - Final video

## How It Works

VidGen uses a five-step pipeline:

1. **Director Agent** - Analyzes prompt and creates shot plan
2. **Scene Agent** - Generates detailed image prompts for each shot
3. **Keyframe Agent** - Creates images using Flux Schnell
4. **Interpolation Agent** - Generates smooth transitions using FILM
5. **Video Assembly** - Combines frames into MP4 at 24fps

## Project Structure

```
VidGen/
├── agents/              # AI agents for each pipeline step
├── models/              # API client wrappers (Claude, Replicate)
├── utils/               # Helper utilities
├── main.py              # CLI entry point
├── orchestrator.py      # Pipeline coordinator
└── requirements.txt     # Dependencies
```

## API Costs

Approximate costs per video (4-8 seconds):
- Claude API: ~$0.01-0.03
- Replicate (Flux): ~$0.10-0.20
- Replicate (FILM): ~$0.01-0.02

**Total: ~$0.12-0.25 per video**

## Requirements

- `anthropic` - Claude API client
- `replicate` - Replicate API client
- `opencv-python` - Video processing
- `python-dotenv` - Environment configuration
- `Pillow` - Image handling
- `requests` - HTTP requests

## Limitations

- Video length: 4-8 seconds (configurable)
- Rate limits: ~12 second delay between API calls
- Output format: MP4 (H.264)
- Aspect ratio: 16:9

## Troubleshooting

### API Key Errors
- Verify keys in `.env` file
- Check [Anthropic Console](https://console.anthropic.com/) for valid key
- Confirm [Replicate account](https://replicate.com/account) has credit

### Generation Failures
- Ensure stable internet connection
- Check Replicate credit balance
- Verify Python 3.8+ is installed

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Acknowledgments

- [Anthropic Claude](https://www.anthropic.com/claude) for scene understanding
- [Black Forest Labs Flux](https://blackforestlabs.ai/) for image generation
- [Google FILM](https://github.com/google-research/frame-interpolation) for interpolation
