#!/usr/bin/env python3
"""
Hermes TTS wrapper — ElevenLabs direct API call with speed=1.15.
Use this instead of the `text_to_speech` tool, which doesn't respect speed config.
"""
import requests, sys

API_KEY = "sk_6d0839f53c5a654e06166101c97695a3d4c0a5099fd233c7"
VOICE_ID = "UT6BK299jzZuhXKDXGoK"
SPEED = 1.2
MODEL = "eleven_multilingual_v2"

def speak(text):
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "speed": SPEED
        }
    }
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        json=payload, headers=headers, timeout=30
    )
    if r.status_code == 200:
        safe = text[:30].replace(" ", "_").replace("\n", "")
        path = f"/data/cache/audio/tts_{safe}.mp3"
        with open(path, "wb") as f:
            f.write(r.content)
        print(f"MEDIA:{path}")
    else:
        print(f"ERROR: {r.status_code} - {r.text[:200]}")

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()
    if text:
        speak(text)
