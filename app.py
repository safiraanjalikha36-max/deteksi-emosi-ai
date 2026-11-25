import streamlit as st
from transformers import pipeline

# 1. Judul Website
st.title("Aplikasi Deteksi Emosional Teks AI 🎭")
st.write("Ketik kalimatmu di bawah ini untuk mendeteksi emosi di dalamnya!")

# 2. Kotak Input Teks untuk Pengguna
kalimat_user = st.text_area("Masukkan kalimat/curhatan di sini:", "Hari ini aku senang sekali karena nilaiku bagus!")

if st.button("Deteksi Emosi ✨"):
    with st.spinner('AI sedang membaca perasaanmu...'):
        # 3. Memuat Model AI khusus pendeteksi emosi
        deteksi_emosi = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")
        
        # 4. Memproses teks dari pengguna
        hasil = deteksi_emosi(kalimat_user)[0]
        
        # 5. Menampilkan hasil emosi ke layar web
        st.write("---")
        st.write("### 🤖 Hasil Analisis Emosi:")
        
        label_emosi = hasil['label'].upper()
        skor_akurasi = hasil['score'] * 100
        
        # Menerjemahkan label emosi ke Bahasa Indonesia
        kamus_emosi = {
            "JOY": "SENANG / BAHAGIA 😊",
            "SADNESS": "SEDIH / HARU 😢",
            "ANGER": "MARAH / KESAL 😡",
            "FEAR": "TAKUT / CEMAS 😨",
            "LOVE": "PENUH CINTA / KAGUM 🥰",
            "SURPRISE": "TERKEJUT / KAGET 😲"
        }
        
        emosi_indo = kamus_emosi.get(label_emosi, label_emosi)
        
        st.success(f"Emosi yang terdeteksi: **{emosi_indo}**")
        st.info(f"Tingkat Keyakinan AI: **{skor_akurasi:.2f}%**")
