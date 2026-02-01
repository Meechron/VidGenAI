"""Director agent that plans video structure and shot composition."""

from agents.base import BaseAgent


class DirectorAgent(BaseAgent):
    """Plans video structure by breaking prompts into shots with camera angles and timing."""

    def __init__(self):
        super().__init__("Director")

    def run(self, user_prompt):
        """Create a shot plan from the user's prompt."""
        self.log(f"Planning video for: {user_prompt}")

        director_prompt = f'''You are a film director planning a short video.

USER'S REQUEST: "{user_prompt}"

Create a shot plan for a 4-8 second video. Break it into 3-5 shots.

Return ONLY valid JSON in this exact format:
{{
    "title": "Short descriptive title",
    "total_duration": <number of seconds>,
    "style": "visual style description (e.g., cinematic, anime, realistic)",
    "shots": [
        {{
            "shot_number": 1,
            "type": "<wide/medium/close-up/extreme-close-up>",
            "duration": <seconds>,
            "description": "What happens in this shot",
            "camera_movement": "<static/pan/zoom/tracking>",
            "elements": ["list", "of", "key", "visual", "elements"]
        }}
    ]
}}

Guidelines:
- Start with an establishing shot (wide) to set the scene
- Use variety in shot types (don't make all shots the same)
- Each shot should have clear visual elements
- Total duration of all shots should equal total_duration
- Keep descriptions vivid but concise

Return ONLY the JSON, no other text.'''

        shot_plan = self.claude.send_structured(director_prompt)

        self.log(f"Created {len(shot_plan['shots'])} shots, {shot_plan['total_duration']}s total")

        return shot_plan
