#Step1: Setup Gemini API key
import os
from dotenv import load_dotenv
load_dotenv(override=True)

import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

#Step2: Convert image to required format (Not strictly needed for Gemini file API but good for base64 local injection)
import base64

def encode_image(image_path):   
    image_file = open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

#Step3: Setup Multimodal LLM 
# model = "gemini-1.5-pro" or "gemini-1.5-flash"
model_name = "gemini-flash-latest"

def analyze_image_with_query(query, model=model_name, encoded_image=None):
    # For Gemini, we can pass image bytes directly or use PIL
    # If encoded_image is passed (base64 string), we decode it back to bytes
    
    parts = [query]
    
    if encoded_image:
        try:
            image_bytes = base64.b64decode(encoded_image)
            image_part = {
                "mime_type": "image/jpeg", # Assuming JPEG as per typical usage, can be made dynamic
                "data": image_bytes
            }
            parts.append(image_part)
        except Exception as e:
            return f"Error decoding image for Gemini: {e}"

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model_instance = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
    )

    chat_session = model_instance.start_chat(
        history=[]
    )

    response = chat_session.send_message(parts)
    return response.text
