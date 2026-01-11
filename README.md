---
title: AI Doctor
emoji: 👨‍⚕️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 3.50.2
app_file: gradio_app.py
pinned: false
license: mit
---

# AI Doctor - Multimodal AI Assistant

An intelligent medical assistant powered by:
- **Brain:** Google Gemini Flash
- **Voice:** ElevenLabs (English/Spanish/French) & Google TTS (Kannada)
- **Hearing:** AssemblyAI

## System Requirements
- **FFmpeg**: This project requires FFmpeg to be installed and available in your system path for audio conversion.
  - **Mac:** `brew install ffmpeg`
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
  - **Linux:** `sudo apt install ffmpeg`

## Setup (Locally)
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Set `.env` variables (see below).
4. Run: `python gradio_app.py`

## Deployment (Hugging Face Spaces)
This repository is configured for HF Spaces.

### Required Secrets
Go to **Settings > Variables & Secrets** in your Space and add:
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID` (Default: `nPczCjzI2devNBz1zQrb`)
- `ELEVENLABS_VOICE_ID_KN` (Kannada: `cQA1lL0fn7iAFW1w50SR`)
- `ASSEMBLYAI_API_KEY`
