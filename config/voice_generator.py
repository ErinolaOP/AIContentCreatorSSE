import os
import requests

def generate_audio(script_data: dict, output_path: str = "generated/audio/voiceover.mp3") -> str:
    """Generates standard voiceover audio using ElevenLabs TTS."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is missing.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    text = script_data.get("narration_text", "")
    
    # Built-in default voice accessible on Free plans (George)
    voice_id = "JBFqnCBsd6RMkjVDRZzb" 
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_flash_v2_5",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print(f"🎙️ Generating TTS audio via ElevenLabs...")
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs API Error ({response.status_code}): {response.text}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Voiceover saved to {output_path}")
    return output_path