import streamlit as st
from transformers import pipeline
from PIL import Image

# 1. Judul Website
st.title("Aplikasi Deteksi Emosi Lewat Wajah AI 📸🎭")
st.write("Unggah foto wajah di bawah ini untuk menebak ekspresi emosinya!")

# 2. Tombol Upload Gambar Wajah
file_gambar = st.file_uploader("Pilih foto wajah (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if file_gambar is not None:
    # Menampilkan gambar wajah yang di-upload ke layar
    gambar = Image.open(file_gambar)
    st.image(gambar, caption='Foto Wajah yang Diunggah', use_column_width=True)
    
    st.write("---")
    st.write("### 🤖 Hasil Analisis Ekspresi Wajah:")
    
    with st.spinner('AI sedang menganalisis ekspresi wajah...'):
        # 3. Memuat Model AI khusus Face Emotion Recognition dari Hugging Face
        deteksi_wajah = pipeline("image-classification", model="dima806/facial_emotions_image_detection")
        hasil = deteksi_wajah(gambar)
        
        # Kamus terjemahan emosi wajah ke Bahasa Indonesia
        kamus_emosi = {
            "sad": "SEDIH 😢",
            "happy": "BAHAGIA / TERSENYUM 😊",
            "angry": "MARAH 😡",
            "surprise": "TERKEJUT / KAGET 😲",
            "fear": "TAKUT / CEMAS 😨",
            "disgust": "JIJIK / JENGKEL 🤢",
            "neutral": "DATAR / BIASA SAJA 😐"
        }
        
        # 4. Menampilkan 3 tebakan ekspresi teratas
        for i, tebakan in enumerate(hasil[:3]):
            label_asal = tebakan['label'].lower()
            emosi_indo = kamus_emosi.get(label_asal, label_asal.upper())
            persentase = tebakan['score'] * 100
            
            if i == 0:
                st.success(f"**Tebakan Utama: {emosi_indo} ({persentase:.2f}%)**")
            else:
                st.write(f"Kemungkinan {i+1}: {emosi_indo} ({persentase:.2f}%)")
