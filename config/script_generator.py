import os
import json
import time
from google import genai
from google.genai.errors import ServerError, APIError

def generate_script(topic: str) -> dict:
    """Generates script, Pexels search terms, title, description, and hashtags."""
    client = genai.Client()
    
    prompt = f"""
    Write a high-retention 30-40 second short-form video script based on this topic: "{topic}".
    
    Return ONLY valid JSON matching this schema:
    {{
      "title": "A catchy viral title under 60 characters",
      "description": "An engaging 2-sentence YouTube description",
      "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
      "narration_text": "The full spoken voiceover text without stage directions.",
      "visual_keywords": ["keyword1", "keyword2", "keyword3", "keyword4"]
    }}
    """

    models_to_try = ["gemini-3.6-flash", "gemini-2.0-flash"]
    
    for model_name in models_to_try:
        for attempt in range(1, 4):
            try:
                print(f"Generating script and metadata using {model_name}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_text)

            except (ServerError, APIError) as e:
                print(f"⚠️ API Server Error on {model_name}. Retrying in {attempt * 2}s...")
                time.sleep(attempt * 2)
            except Exception as e:
                print(f"❌ Error on {model_name}: {e}")
                break

    raise RuntimeError("Failed to generate script after multiple retry attempts.")