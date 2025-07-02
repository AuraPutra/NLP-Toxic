import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import text, sequence
import numpy as np
import pickle

# Load model
model_path = 'model.h5'
model = load_model(model_path)

with open("tokenizer.pkl", "rb") as f:
    token = pickle.load(f)

max_len = 1500

# Fungsi prediksi
def predict_toxicity(comment):
    comment_seq = token.texts_to_sequences([comment])
    comment_pad = sequence.pad_sequences(comment_seq, maxlen=max_len)
    prediction = model.predict(comment_pad)
    return prediction[0][0]

# Contoh input
input_text = "halo nama saya"

# Prediksi
prob = predict_toxicity(input_text)
predicted_class = int(prob > 0.8)

print("Prediksi probabilitas:", prob)
print("Prediksi kelas (threshold 0.8):", predicted_class)