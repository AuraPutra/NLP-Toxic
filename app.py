from flask import Flask, render_template, request, jsonify
from elevenlabs import ElevenLabs, VoiceSettings
from keras.models import load_model
from keras.preprocessing import sequence
import pickle
import os
import speech_recognition as sr

from API_KEY import API_KEY_EL, API_KEY_GROK

app = Flask(__name__)
eleven = ElevenLabs(api_key=API_KEY_EL)

model = load_model('model/gru_toxic_model.h5')
with open("model/tokenizer.pkl", "rb") as f:
    token = pickle.load(f)
max_len = 1500

@app.route("/")
def index():
    return render_template("index.html")

def predict_toxicity(comment):
    seq = token.texts_to_sequences([comment])
    pad = sequence.pad_sequences(seq, maxlen=max_len)
    prob = float(model.predict(pad)[0][0])
    return prob

def generate_voice(text):
    voice_path = os.path.join("static", "voice.mp3")
    audio = eleven.text_to_speech.convert(
        voice_id="RWiGLY9uXI70QL540WNd",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )
    with open(voice_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)
    return voice_path

def proses_paraphrase(text):
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.core.credentials import AzureKeyCredential
    # Konfigurasi koneksi
    endpoint = "https://models.github.ai/inference"
    model = "xai/grok-3"
    token = API_KEY_GROK
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )
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
            UserMessage(text),
        ],
        temperature=0.6,
        top_p=0.9,
        model=model,
        max_tokens=512,
        frequency_penalty=0.2,
        presence_penalty=0.4,
    )
    return response.choices[0].message.content

@app.route("/predict", methods=["POST"])
def predict():
    text = request.json.get("text", "")
    prob = predict_toxicity(text)
    label = int(prob > 0.8)
    final_text = f"{text} itu {'Toxic' if label else 'Tidak Toxic'}"
    generate_voice(final_text)
    teks_paraphrase = proses_paraphrase(text)
    return jsonify({
        "text": text,
        "text_paraphrase": teks_paraphrase,
        "label": label,
        "probability": prob,
        "audio_url": "/static/voice.mp3"
    })

@app.route("/predict_audio", methods=["POST"])
def predict_audio():

    from pydub.utils import which
    from pydub import AudioSegment
    # Path ke direktori ffmpeg lokal (dalam folder proyek)
    ffmpeg_dir = os.path.abspath("f/bin")

    # Tambahkan ke PATH lingkungan (sementara, hanya saat script berjalan)
    os.environ["PATH"] += os.pathsep + ffmpeg_dir

    # Set path spesifik ke pydub
    AudioSegment.converter = which("ffmpeg.exe")
    AudioSegment.ffprobe = which("ffprobe.exe")

    file = request.files["audio"]
    audio_path = "temp.webm"
    file.save(audio_path)

    sound = AudioSegment.from_file(audio_path)
    sound.export("temp.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return jsonify({"error": "Tidak bisa mengenali suara"}), 400

    prob = predict_toxicity(text)
    label = int(prob > 0.8)
    final_text = f"{text} itu {'Toxic' if label else 'Tidak Toxic'}"
    generate_voice(final_text)


    teks_paraphrase = proses_paraphrase(text)
    print(teks_paraphrase)
    return jsonify({
        "text": text,
        "text_paraphrase": teks_paraphrase,
        "label": label,
        "probability": prob,
        "audio_url": "/static/voice.mp3"
    })



if __name__ == "__main__":
    app.run(debug=True, port=80)
