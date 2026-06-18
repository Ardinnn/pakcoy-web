import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tf_keras as keras_aman  # Cukup panggil 1 Keras ini untuk kedua model
import numpy as np
import joblib
from PIL import Image
import io

app = Flask(__name__)
CORS(app) 

print("\n--- MENYIAPKAN SERVER AI ---")
print("1. Memuat Model CNN (Teachable Machine)...")
model_cnn = keras_aman.models.load_model('keras_model.h5', compile=False)

with open('labels.txt', 'r') as f:
    labels = f.read().splitlines()

print("2. Memuat Model LSTM dan Scaler...")
# Sekarang LSTM dibaca dengan mesin yang sama persis seperti CNN
model_lstm = keras_aman.models.load_model('model_lstm_pakcoy.h5')
scaler = joblib.load('scaler_pakcoy.pkl')

print("--- SERVER SIAP MENERIMA REQUEST ---\n")

# ==========================================
# ENDPOINT 1: KLASIFIKASI GAMBAR (TEACHABLE MACHINE)
# ==========================================
@app.route('/predict-image', methods=['POST'])
def predict_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar yang dikirim'}), 400
    
    file = request.files['file']
    
    try:
        img = Image.open(io.BytesIO(file.read())).convert('RGB')
        img = img.resize((224, 224)) 
        
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = (img_array / 127.5) - 1 

        prediksi = model_cnn.predict(img_array)
        indeks_tertinggi = np.argmax(prediksi)
        
        label_kotor = labels[indeks_tertinggi]
        label_bersih = label_kotor.split(' ', 1)[1] if ' ' in label_kotor else label_kotor
        
        akurasi = float(prediksi[0][indeks_tertinggi] * 100)

        return jsonify({
            'status': 'success',
            'prediksi': label_bersih,
            'akurasi': round(akurasi, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==========================================
# ENDPOINT 2: PREDIKSI SENSOR (LSTM LOKAL)
# ==========================================
@app.route('/predict-sensor', methods=['POST'])
def predict_sensor():
    data = request.json
    if not data or 'history' not in data:
        return jsonify({'error': 'Data history tidak ditemukan'}), 400
    
    history = np.array(data['history'])
    if len(history) != 10:
        return jsonify({'error': 'Data history harus berjumlah persis 10 interval (baris)'}), 400
        
    try:
        history_scaled = scaler.transform(history)
        input_lstm = np.expand_dims(history_scaled, axis=0)
        prediksi_scaled = model_lstm.predict(input_lstm)
        
        dummy = np.zeros((1, 2))
        dummy[0, 0] = prediksi_scaled[0][0] 
        prediksi_asli = scaler.inverse_transform(dummy)[0, 0]
        
        return jsonify({
            'status': 'success',
            'prediksi_kelembapan_selanjutnya': round(float(prediksi_asli), 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)