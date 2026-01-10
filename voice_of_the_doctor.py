import os
import logging
from gtts import gTTS
from elevenlabs import save
from elevenlabs.client import ElevenLabs

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
    # Fetch credentials inside the function to ensure latest env vars are used
    elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
    
    # 🚨 Special Handling: Use Google TTS for Kannada (kn) as per user request
    if lang == "kn":
        logging.info("🔹 Kannada detected. Using Google TTS (gTTS) instead of ElevenLabs.")
        return text_to_speech_with_gtts(input_text, output_filepath, lang)

    # DEBUGGING: Print all keys starting with ELEVENLABS_VOICE_ID
    # logging.info(f"DEBUG: Enviroment keys: {[k for k in os.environ.keys() if k.startswith('ELEVENLABS_VOICE_ID')]}")
    
    # Check for language-specific voice ID first (e.g., ELEVENLABS_VOICE_ID_ES)
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
        client = ElevenLabs(api_key=elevenlabs_key)

        model = "eleven_multilingual_v2" if lang != "en" else "eleven_turbo_v2"
        voice = voice_id if voice_id else "Aria"

        audio = client.generate(
            text=input_text,
            voice=voice,
            model=model,
            output_format="mp3_22050_32"
        )

        save(audio, output_filepath)
        logging.info(f"ElevenLabs audio saved at {output_filepath} (voice={voice}, model={model})")
        return output_filepath

    except Exception as e:
        logging.error(f"ElevenLabs TTS failed: {e}. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath, lang)