import os
import logging
from gtts import gTTS
# Imports handled inside functions for safety

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Removed global API key retrieval to fetch inside function for freshness
# ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
# ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID")


# -------------------------------
# Google TTS (fallback)
# -------------------------------
def text_to_speech_with_gtts(input_text: str, output_filepath: str = "final.mp3", lang: str = "en"):
    try:
        tts = gTTS(text=input_text, lang=lang, slow=False)
        tts.save(output_filepath)
        logging.info(f"gTTS audio saved at {output_filepath} (lang={lang})")
        return output_filepath
    except Exception as e:
        logging.error(f"gTTS failed: {e}")
        raise


# -------------------------------
# ElevenLabs TTS (primary)
# -------------------------------
def text_to_speech_with_elevenlabs(input_text: str, output_filepath: str = "final.mp3", lang: str = "en"):
    # Fetch credentials inside the function
    elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
    
    # 🚨 Special Handling: Use Google TTS for Kannada (kn) as per user request
    if lang == "kn":
        logging.info("🔹 Kannada detected. Using Google TTS (gTTS) instead of ElevenLabs.")
        return text_to_speech_with_gtts(input_text, output_filepath, lang)

    # Check for language-specific voice ID
    env_var_name = f"ELEVENLABS_VOICE_ID_{lang.upper()}"
    voice_id = os.environ.get(env_var_name)
    
    if not voice_id:
        logging.info(f"No override found for {env_var_name}. Using default.")
        voice_id = os.environ.get("ELEVENLABS_VOICE_ID")
    else:
        logging.info(f"Using language-specific voice ID for {lang}: {voice_id}")

    if not elevenlabs_key:
        logging.warning("ELEVENLABS_API_KEY not found. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath, lang)

    try:
        import requests
        
        # Default voice (Aria) if none specified
        if not voice_id:
            voice_id = "21m00Tcm4TlvDq8ikWAM" # Rachel default, or use Aria ID if known

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "xi-api-key": elevenlabs_key,
            "Content-Type": "application/json"
        }
        
        model = "eleven_multilingual_v2" if lang != "en" else "eleven_turbo_v2"
        
        data = {
            "text": input_text,
            "model_id": model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(output_filepath, "wb") as f:
                f.write(response.content)
            logging.info(f"ElevenLabs audio saved at {output_filepath} (voice={voice_id}, model={model}) via API")
            return output_filepath
        else:
            logging.error(f"ElevenLabs API Error: {response.status_code} - {response.text}")
            return text_to_speech_with_gtts(input_text, output_filepath, lang)

    except Exception as e:
        logging.error(f"ElevenLabs TTS failed: {e}. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath, lang)