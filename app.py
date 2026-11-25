import streamlit as st
from transformers import pipeline
from PIL import Image

# 1. JUDUL & KONFIGURASI HALAMAN
st.set_page_config(page_title="Asisten AI Interaktif", page_icon="🤖")
st.title("🤖 Asisten AI Pintar")
st.write("Unggah fotomu untuk dideteksi, lalu kamu bisa bertanya apa saja pada asisten!")

# Menginisialisasi riwayat pesan chat agar tidak hilang saat diklik
if "messages" not in st.session_state:
    st.session_state.messages = []
if "emosi_terdeteksi" not in st.session_state:
    st.session_state.emosi_terdeteksi = "Belum ada foto yang dianalisis"

# 2. PANEL UNTUK UNGGAH FOTO
file_gambar = st.file_uploader("Pilih foto (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if file_gambar is not None:
    gambar = Image.open(file_gambar)
    st.image(gambar, caption='Foto yang Diunggah', width=300)
    
    # Jalankan deteksi otomatis (Contoh di bawah menggunakan model ekspresi wajah)
    with st.spinner('AI sedang menganalisis foto...'):
        deteksi_wajah = pipeline("image-classification", model="dima806/facial_emotions_image_detection")
        hasil = deteksi_wajah(gambar)
        
        kamus_emosi = {
            "sad": "Sedih 😢", "happy": "Bahagia/Tersenyum 😊", "angry": "Marah 😡",
            "surprise": "Terkejut 😲", "fear": "Takut/Cemas 😨", "neutral": "Datar/Biasa saja 😐"
        }
        
        label_asal = hasil[0]['label'].lower()
        st.session_state.emosi_terdeteksi = kamus_emosi.get(label_asal, label_asal.upper())
        
        st.success(f"**Hasil deteksi terbaru: Wajah kamu tampak {st.session_state.emosi_terdeteksi}**")

st.write("---")

# 3. CHATBOT INTERAKTIF (PERSIS SEPERTI DI GAMBAR TEMANMU)
st.write(f"### 💬 Asisten AI")
st.write(f"*Status Deteksi Terakhir: {st.session_state.emosi_terdeteksi}*")

# Menampilkan riwayat obrolan di layar website
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Tombol Pilihan Otomatis (Quick Replies) agar user tinggal klik
st.write("💡 *Pertanyaan Cepat:*")
kolom1, kolom2, kolom3 = st.columns(3)

tombol_ditekan = None
if kolom1.button("Ciri emosi ini"):
    tombol_ditekan = f"Apa saja ciri-ciri visual dari ekspresi wajah {st.session_state.emosi_terdeteksi}?"
if kolom2.button("Tips menenangkan diri"):
    tombol_ditekan = "Berikan tips mudah untuk menenangkan pikiran dan emosi saat ini."
if kolom3.button("Rekomendasi aktivitas"):
    tombol_ditekan = f"Apa aktivitas atau hiburan yang cocok untuk orang yang sedang merasa {st.session_state.emosi_terdeteksi}?"

# Kotak tempat mengetik pertanyaan manual
pertanyaan_manual = st.chat_input("Tulis pertanyaan harianmu di sini...")

# Memproses jika ada tombol yang diklik atau teks yang diketik
input_user = pertanyaan_manual or tombol_ditekan

if input_user:
    # Tampilkan chat dari pengguna
    st.session_state.messages.append({"role": "user", "content": input_user})
    with st.chat_message("user"):
        st.markdown(input_user)
        
    # Generate jawaban simulasi pintar dari asisten (menyesuaikan hasil deteksi foto)
    with st.chat_message("assistant"):
        st.write("🤖 *Asisten sedang mengetik...*")
        
        # Logika jawaban otomatis pintar tanpa perlu API berbayar
        if "ciri" in input_user.lower():
            jawaban_ai = f"Secara umum, kondisi {st.session_state.emosi_terdeteksi} dapat terlihat dari kerutan dahi, bentuk bibir yang melengkung, serta tatapan mata. AI mendeteksinya berdasarkan jutaan pola piksel gambar wajah internasional."
        elif "tips" in input_user.lower() or "menenangkan" in input_user.lower():
            jawaban_ai = "Tips terbaik saat ini: \n1. Atur napas dalam-dalam (metode 4-7-8).\n2. Istirahat sejenak dari layar hp/laptop.\n3. Minum segelas air putih hangat."
        elif "aktivitas" in input_user.lower() or "rekomendasi" in input_user.lower():
            jawaban_ai = f"Untuk kondisi {st.session_state.emosi_terdeteksi}, disarankan mencoba jalan santai di ruangan terbuka, mendengarkan musik instrumental yang tenang, atau membaca buku favorit kamu."
        else:
            jawaban_ai = f"Terima kasih atas pertanyaannya! Terkait kondisi foto yang terdeteksi ({st.session_state.emosi_terdeteksi}), sangat disarankan untuk menjaga suasana hati agar tetap positif dan rileks ya!"
            
        st.markdown(jawaban_ai)
        st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})
