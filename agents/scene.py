"""Scene agent that creates detailed image prompts from shot plans."""

from agents.base import BaseAgent


class SceneAgent(BaseAgent):
    """Creates detailed image generation prompts from shot plans."""

    def __init__(self):
        super().__init__("Scene")

    def run(self, shot_plan):
        """Create detailed image prompts from the shot plan."""
        self.log(f"Creating prompts for {len(shot_plan['shots'])} shots")

        scene_prompt = f'''You are an expert at writing prompts for AI image generation (Flux/Stable Diffusion).

VIDEO TITLE: "{shot_plan['title']}"
STYLE: {shot_plan['style']}

SHOT PLAN:
{self._format_shots(shot_plan['shots'])}

For each shot, create 1-2 keyframe prompts. Each keyframe should be a detailed image prompt.

Return ONLY valid JSON in this exact format:
{{
    "title": "{shot_plan['title']}",
    "style": "{shot_plan['style']}",
    "keyframes": [
        {{
            "keyframe_id": "shot1_key1",
            "shot_number": 1,
            "timestamp": 0.0,
            "prompt": "Detailed prompt for AI image generation, include style, lighting, camera angle, quality tags",
            "negative_prompt": "Things to avoid: blurry, low quality, distorted, etc.",
            "elements": ["key", "visual", "elements"],
            "notes": "Any special considerations"
        }}
    ]
}}

PROMPT WRITING GUIDELINES:
1. Be specific and detailed (50-100 words per prompt)
2. Include style keywords: cinematic, photorealistic, 8k, detailed, etc.
3. Describe lighting: dramatic lighting, golden hour, backlit, etc.
4. Include camera/composition: wide shot, close-up, low angle, etc.
5. Add quality boosters: highly detailed, professional, masterpiece
6. Keep consistent style across all keyframes
7. For negative prompts: include common issues to avoid

Return ONLY the JSON, no other text.'''

        scene_data = self.claude.send_structured(scene_prompt)
        self.log(f"Created {len(scene_data['keyframes'])} keyframe prompts")

        return scene_data

    def _format_shots(self, shots):
        """Format shots into a readable string for the prompt."""
        formatted = []
        for shot in shots:
            formatted.append(f"""
Shot {shot['shot_number']}:
  - Type: {shot['type']}
  - Duration: {shot['duration']} seconds
  - Description: {shot['description']}
  - Camera: {shot.get('camera_movement', 'static')}
  - Elements: {', '.join(shot['elements'])}
""")
        return '\n'.join(formatted)
