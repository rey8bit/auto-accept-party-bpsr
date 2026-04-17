# BPSR Auto-Accept Party Tool

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Game](https://img.shields.io/badge/Game-Blue%20Protocol%3A%20Star%20Resonance-orange)](https://blue-protocol.com/)

Alat bantu otomatisasi ringan dengan antarmuka modern (Dark Mode) untuk menerima permintaan party secara otomatis di **Blue Protocol: Star Resonance**.

---

## 📸 Preview Interface

| Full Mode (Active) | Mini Mode |
|---|---|
| ![Full UI](app2.png) | ![Mini Mode](appmini.png) |

*Tampilan log yang detail memantau resolusi layar dan status fokus jendela game.*

---

## ✨ Fitur Unggulan

- 🌑 **Full Dark Mode**: Antarmuka "Midnight Stealth" yang nyaman di mata.
- 📱 **Modular UI**:
  - **Mini Mode**: Mengecilkan jendela agar tidak mengganggu pandangan saat bermain.
  - **Log Toggle**: Sembunyikan atau tampilkan log aktivitas sesukamu.
- 🎯 **Focus Awareness**: Skrip hanya akan memindai layar jika jendela `StarSEA_Steam.exe` sedang aktif (mencegah salah input saat Alt-Tab).
- 📌 **Top Toggle**: Menjaga aplikasi tetap melayang di atas jendela game.
- ⚡ **Optimized Performance**: Penggunaan CPU yang sangat rendah dengan sistem *Adaptive Scanning*.

---

## 🛠️ Persiapan (Build dari Source)

Karena repositori ini **hanya menyertakan kode sumber** demi keamanan dan transparansi, kamu perlu membangunnya sendiri:

### 1. Prasyarat
- Instal [Python 3.10 atau lebih baru](https://www.python.org/downloads/).
- Pastikan kamu berada di folder proyek setelah melakukan clone/download.

### 2. Instalasi Dependensi
Buka terminal/CMD di folder proyek dan jalankan:
```bash
pip install -r requirements.txt
