import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def recommend(query: str, songs: list[dict]) -> str:
    song_list = "\n".join([
        f"- {s['track_name']} by {s['artists']} | Genre: {s['track_genre']} | Popularity: {s['popularity']}"
        for s in songs
    ])

    prompt = f"""You are a music recommendation assistant.

A user is looking for: "{query}"

Based on their request, here are the most relevant songs found:
{song_list}

Write a warm, conversational recommendation. Mention each song by name, and give a one-sentence description of why it fits what the user is looking for. Keep it concise and friendly."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        result = response.choices[0].message.content
        logging.info("Recommendation generated successfully")
        return result

    except Exception as e:
        logging.error(f"Recommendation failed: {e}")
        raise
