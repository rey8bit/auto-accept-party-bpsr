# BPSR Auto-Accept Party Tool

[English](README.md) / **Bahasa Indonesia**

# BPSR Auto-Accept Party Tool

Alat otomatisasi *open-source* yang ringan untuk menerima undangan *party* secara otomatis di **Blue Protocol: Star Resonance**.

### ✨ Fitur Utama
- **Auto-Scale**: Mendukung semua resolusi layar (1080p, 900p, 720p, dll.) tanpa pengaturan tambahan.
- **ESP Overlay**: Indikator kotak visual untuk melacak area pemindaian dan target.
- **MSS + OpenCV**: Deteksi gambar super cepat dengan penggunaan CPU yang sangat rendah.
- **Multi-Bahasa**: Terjemahan mudah melalui file JSON di folder `lang/`.
- **Mode Mini**: Tampilan ringkas untuk menghemat ruang layar.

### ⌨️ Tombol Cepat (Hotkeys)
- **F9**: Mulai Pemindaian
- **F10**: Berhenti Memindai
- **F11**: Aktifkan/Matikan Mode Selalu di Atas (Always-on-Top)

### 🛠️ Instalasi & Cara Menggunakan
Karena alat ini didistribusikan sebagai kode sumber demi transparansi, kamu membutuhkan Python untuk menjalankan atau melakukan *compile*:
1. Instal [Python 3.10+](https://www.python.org/downloads/).
2. Kloning/unduh repositori ini.
3. Instal pustaka yang dibutuhkan dengan menjalankan: `pip install -r requirements.txt`
4. Letakkan gambar targetmu (contoh: `party_request.png`) di folder aplikasi.
Contoh: Gambar yang di-*crop* ini diambil pada resolusi 1080p.
![Contoh](party_request_1080.png)
5. Jalankan skrip melalui terminal: `python bpsr_auto_accept_gui.py` (atau jadikan `.exe` sendiri menggunakan PyInstaller).
6. Tekan **F9** atau klik tombol *play* untuk menjalankan aplikasi.

---
*Dioptimalkan untuk `StarSEA_Steam.exe`, tetapi kamu bisa mengubahnya untuk klien mandiri (standalone) dengan mengedit skrip. Gunakan dengan risiko ditanggung sendiri.*