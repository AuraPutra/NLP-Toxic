import speech_recognition as sr
import pyttsx3
import os
from gtts import gTTS
import pygame
import time

# Inisialisasi recognizer dan text-to-speech engine
r = sr.Recognizer()
tts = pyttsx3.init()

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

with sr.Microphone() as source:
    print("Silakan bicara...")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='en-EN')
        print("Anda berkata:", text)
        bicara(text)
    except sr.UnknownValueError:
        print("Maaf, suara tidak dikenali.")
        tts.say("Maaf, suara tidak dikenali.")
        tts.runAndWait()
    except sr.RequestError:
        print("Gagal terhubung ke layanan.")
        tts.say("Gagal terhubung ke layanan.")
        tts.runAndWait()

