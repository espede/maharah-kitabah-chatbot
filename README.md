# 🤖 Chatbot Pembelajaran Maharah Kitabah

Chatbot interaktif untuk belajar **Maharah Kitabah** (مهارة الكتابة) — keterampilan menulis dalam bahasa Arab. Didukung oleh AI dari [B.AI](https://chat.b.ai).

## ✨ Fitur

- **🖊️ Mode Belajar** — Penjelasan konsep menulis Arab dengan contoh
- **✍️ Mode Latihan** — Latihan menulis dengan koreksi otomatis
- **📝 Mode Koreksi** — Koreksi teks Arab yang kamu tulis
- **🧠 Mode Kuis** — Kuis interaktif tentang menulis Arab
- **💬 Chat Bebas** — Tanya apa saja tentang Maharah Kitabah
- **🎨 Rich Terminal UI** — Tampilan terminal yang cantik dengan emoji & warna

## 📋 Topik yang Dibahas

- Jenis-jenis tulisan Arab (Naskh, Riq'ah, Tsuluts, dll)
- Kaidah penulisan huruf Arab
- Harakat (Fathah, Kasrah, Dhammah, dll)
- Penulisan kata dan kalimat
- Qawaid al-Kitabah (kaidah menulis)
- Tata bahasa terkait menulis
- Tips dan trik menulis Arab yang baik

## 🚀 Instalasi

```bash
# 1. Clone repositori
git clone https://github.com/espede/maharah-kitabah-chatbot.git
cd maharah-kitabah-chatbot

# 2. Buat virtual environment (opsional tapi direkomendasikan)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup API Key
cp .env.example .env
# Edit .env dan masukkan API key dari https://chat.b.ai
```

## 🔑 Mendapatkan API Key

1. Kunjungi https://chat.b.ai
2. Daftar/Login akun
3. Buka halaman **API** di sidebar
4. Generate API Key baru
5. Copy dan paste ke file `.env`

## 💻 Penggunaan

### Mode Interaktif (Default)
```bash
python chatbot.py
```

### Mode Spesifik
```bash
# Mode belajar
python chatbot.py --mode belajar

# Mode latihan
python chatbot.py --mode latihan

# Mode koreksi
python chatbot.py --mode koreksi

# Mode kuis
python chatbot.py --mode kuis
```

### Contoh Penggunaan
```bash
# Chat bebas tentang Maharah Kitabah
python chatbot.py --mode bebas

# Koreksi teks langsung
python chatbot.py --mode koreksi
```

## 📸 Preview

```
╔══════════════════════════════════════════════════════════════╗
║        🤖 CHATBOT PEMBELAJARAN MAHARAH KITABAH              ║
║           مهارة الكتابة - Keterampilan Menulis Arab           ║
║                  Powered by B.AI                            ║
╚══════════════════════════════════════════════════════════════╝

📋 MENU PEMBELAJARAN:
──────────────────────────────────────
  1  🖊️   Mode Belajar     - Pelajari konsep menulis Arab
  2  ✍️   Mode Latihan     - Latihan menulis dengan koreksi
  3  📝   Mode Koreksi     - Koreksi tulisan Arab kamu
  4  🧠   Mode Kuis        - Uji pemahaman dengan kuis
  5  💬   Chat Bebas       - Tanya apa saja
  6  ❌   Keluar
```

## ⚙️ Konfigurasi

Edit file `.env` untuk mengkonfigurasi:

```env
# API Key dari B.AI (wajib)
BAI_API_KEY=your_api_...

# Model AI yang digunakan (opsional)
BAI_MODEL=MiniMax-M3

# Bahasa respons (id=en, ar=arab, id=indonesia)
DEFAULT_LANG=id

# Panjang respons maksimal (opsional)
MAX_TOKENS=2048
```

## 📁 Struktur Project

```
maharah-kitabah-chatbot/
├── chatbot.py           # Main chatbot application
├── requirements.txt     # Python dependencies
├── .env.example         # Template environment variables
├── .env                 # Environment variables (jangan di-commit!)
├── .gitignore           # Git ignore rules
└── README.md            # Dokumentasi ini
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repositori ini
2. Buat branch baru (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Tambah fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## 📝 Lisensi

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

## 🙏 Acknowledgments

- [B.AI](https://chat.b.ai) — API AI yang digunakan
- Para ulama bahasa Arab yang telah menyusun kaidah menulis
- Komunitas pembelajar bahasa Arab

---

**_CATATAN:_** Chatbot ini adalah alat bantu belajar. Untuk pembelajaran yang lebih mendalam, disarankan untuk tetap belajar dengan guru/ustadz yang kompeten.
