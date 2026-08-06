from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_script(topic):
    prompt = f"""
    You are a TikTok content creator.

    Create a 45-second TikTok script about:

    {topic}

    Requirements:
    - Start with a strong hook in the first 3 seconds
    - Keep sentences short
    - Make it engaging
    - End with a call to action
    """

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content