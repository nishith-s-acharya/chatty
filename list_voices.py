import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.environ.get("ELEVENLABS_API_KEY")

if not api_key:
    print("No API key found")
else:
    client = ElevenLabs(api_key=api_key)
    response = client.voices.get_all()
    # Handle possible structure of response
    if hasattr(response, 'voices'):
        voices = response.voices
    else:
        voices = response

    print(f"{'Name':<20} | {'Voice ID':<30} | {'Category'}")
    print("-" * 65)
    for voice in voices:
        print(f"{voice.name:<20} | {voice.voice_id:<30} | {voice.category}")
