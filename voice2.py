import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import pygame
import time

ELEVENLABS_API_KEY = "sk_6c6b129dabf8059a8b40c3d2fe2b8f54525adc0024d3fa07"
elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)


def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = elevenlabs.text_to_speech.convert(
        voice_id="RWiGLY9uXI70QL540WNd", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )

    # uncomment the line below to play the audio back

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    pygame.mixer.init()
    pygame.mixer.music.load(save_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(save_file_path)
    return save_file_path

text_to_speech_file("Hey friend, I'm really upset with you, and I feel like you're one of the most difficult people I've encountered. I wish you'd reconsider your actions.")
