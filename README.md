# YouTube Production Factory (Autonomous)

This repository contains the autonomous video production framework for creating professional YouTube videos using AI.

## Project Structure
- `master_prompt.txt`: The core instruction set for the AI Assistant.
- `video_factory.py`: The Python engine that handles TTS, Image Generation, and Video Assembly.
- `requirements.txt`: Necessary Python libraries.
- `assets/`: Folder for music, SFX, and generated images.
- `outputs/`: Final rendered videos.

## How to use
1. Connect this repository to your Arena AI Agent.
2. Provide the `Channel Name`, `Video Title`, and `Full Script`.
3. The Agent will use `video_factory.py` to generate the complete video following the "6-second visual slot" rule.

## Rules
- Resolution: 854x480 (SD) for fast rendering.
- Visuals: Changes every 6 seconds.
- Audio: Master voiceover (master_voiceover.mp3) with background music at -29dB.
