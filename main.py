import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import os
from gtts import gTTS
import pygame
import time

def bicara(teks):
    print(f"Jawaban: {teks}")
    tts = gTTS(teks, lang="en")
    tts.save("jawaban.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("jawaban.mp3")
    pygame.mixer.music.play()

    # Tunggu sampai selesai diputar
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Stop mixer sebelum hapus file
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove("jawaban.mp3")
    
load_dotenv()

# Konfigurasi koneksi
endpoint = "https://models.github.ai/inference"
model = "xai/grok-3"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# r = sr.Recognizer()
# tts = pyttsx3.init()

# with sr.Microphone() as source:
#     print("Silakan bicara...")
#     audio = r.listen(source)
#     try:
#         # Kalimat toxic yang akan diparafrase
#         # toxic_input = r.recognize_google(audio, language='en-EN')
#         toxic_input = "I hate you so much, you are the worst person ever! Kill yourself!"

#         # Permintaan ke model
#         response = client.complete(
#             messages=[
#                 SystemMessage(
#                     "You are a language moderation assistant. "
#                     "Your task is to paraphrase toxic, hateful, offensive, or vulgar words and sentences "
#                     "into polite, neutral, and respectful language while maintaining the original meaning as much as possible. "
#                     "Keep the output concise. Do not remove content; rephrase it. "
#                     "If input is a single word, reply with a single polite word. "
#                     "Keep the number of sentences close to the original."
#                 ),
#                 UserMessage(toxic_input),
#             ],
#             temperature=0.6,
#             top_p=0.9,
#             model=model,
#             max_tokens=512,
#             frequency_penalty=0.2,
#             presence_penalty=0.4,
#         )

#         # Cetak hasil parafrase
#         print("Original:", toxic_input)
#         print("Paraphrased:", response.choices[0].message.content)
#         bicara(response.choices[0].message.content)
        
#     except sr.UnknownValueError:
#         print("Maaf, suara tidak dikenali.")
#         tts.say("Maaf, suara tidak dikenali.")
#         tts.runAndWait()
#     except sr.RequestError:
#         print("Gagal terhubung ke layanan.")
#         tts.say("Gagal terhubung ke layanan.")
#         tts.runAndWait()
        
toxic_input = "Ah payah banget lu, goblok! Gak ada otak ya? Semua yang lu bilang cuma sampah! TOLOL BANGET!! NIGGA!"

# Permintaan ke model
response = client.complete(
    messages=[
        SystemMessage(
            "You are a language moderation assistant. "
            "Your task is to paraphrase toxic, hateful, offensive, or vulgar words and sentences "
            "into polite, neutral, and respectful language while maintaining the original meaning as much as possible. "
            "Keep the output concise. Do not remove content; rephrase it. "
            "If input is a single word, reply with a single polite word. "
            "Keep the number of sentences close to the original."
            "Keep the tone of the sentence"
        ),
        UserMessage(toxic_input),
    ],
    temperature=0.6,
    top_p=0.9,
    model=model,
    max_tokens=512,
    frequency_penalty=0.2,
    presence_penalty=0.4,
)

# Cetak hasil parafrase
print("Original:", toxic_input)
print("Paraphrased:", response.choices[0].message.content)
bicara(response.choices[0].message.content)