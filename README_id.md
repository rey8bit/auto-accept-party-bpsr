# BPSR Auto-Accept Party Tool (Experimental)

Alat bantu otomatisasi ringan dengan antarmuka modern (**Dark Mode**) untuk menerima permintaan party secara otomatis di **Blue Protocol: Star Resonance**.
Hanya tersedia dalam bahasa Indonesia saja dan client khusus Steam.

Alat ini dirancang untuk memudahkan pemain menerima permintaan party secara otomatis ketika fokus ke layar game, menggunakan deteksi gambar yang efisien.

### 📸 Pratinjau Antarmuka
| Mode Penuh (Aktif) | Mode Mini |
|---|---|
| ![Full UI](app2.png) | ![Mini Mode](appmini.png) |

### ✨ Fitur Unggulan
- **Full Dark Mode**: Tema gelap "Midnight Stealth" yang nyaman di mata untuk sesi gaming lama.
- **Modular UI**: Pindah ke **Mini Mode** untuk tampilan yang sangat ringkas di pojok layar.
- **Log Toggle**: Tampilkan atau sembunyikan riwayat aktivitas deteksi sesuai kebutuhan.
- **Focus Awareness**: Skrip hanya akan memindai layar jika jendela game (`StarSEA_Steam.exe`) sedang aktif. Otomatis **Standby** saat Alt-Tab.
- **Top Toggle**: Tombol "**Top**" untuk menjaga jendela aplikasi tetap melayang di atas jendela game.
- **Optimasi Performa**: Penggunaan CPU rendah dengan logika pemindaian adaptif.

### 🛠️ Cara Instalasi & Build
1. Instal [Python 3.10+](https://www.python.org/downloads/).
2. Unduh repositori ini dan buka terminal/CMD di folder tersebut.
3. Jalankan perintah berikut untuk menginstal library:
   ```bash
   pip install -r requirements.txt
