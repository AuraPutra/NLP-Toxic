import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

model_path = 'model.h5'  # Pastikan file ini ada!
model = load_model(model_path)

input_text = "halo nama saya"
input_array = np.zeros((1, 10))  # Ganti dengan preprocessing yang benar

prediction = model.predict(input_array)
predicted_class = (prediction > 0.8).astype(int)

print("Prediksi probabilitas:", prediction)
print("Prediksi kelas (threshold 0.8):", predicted_class)