import ctypes
# --- SIHIR ANTI-BUG DPI ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    app_id = 'bpsr.autoaccept.partytool.test'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except Exception:
    pass

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import pydirectinput
import keyboard
import pyautogui
import time
import win32gui
import win32con
import configparser
import os
import random
import winsound
import json
from datetime import datetime

# Library optimisasi pemindaian gambar
import mss
import cv2
import numpy as np

# ================= INISIALISASI BAHASA OTOMATIS =================
def inisialisasi_folder_bahasa():
    """Membuat folder lang/ dan file bahasanya secara otomatis jika belum ada"""
    if not os.path.exists("lang"):
        os.makedirs("lang")

    # Data Bahasa Indonesia (Default)
    teks_id = {
        "title": "BPSR Alat Auto-Accept Party",
        "header": "ALAT BPSR AUTO-ACCEPT PARTY",
        "start": "MULAI (F9)",
        "stop": "BERHENTI (F10)",
        "ontop": "📌 Top",
        "mini": "🗕 Mini",
        "full": "🗖 Penuh",
        "log_on": "📝 Log: ON",
        "log_off": "📝 Log: OFF",
        "btn_clear": "🗑️ Hapus Log",    
        "settings": "⚙️",               
        "status_ready": "Status: Siap / Terhenti",
        "status_search": "Status: Sedang Berjalan (Mencari Game)",
        "status_scan": "Status: Sedang Berjalan (Memindai Game Dinamis)",
        "status_standby": "Status: Siaga (Menunggu Fokus)",
        "log_ready": "Sistem Siap. Menunggu instruksi.",
        "log_ontop_on": "Selalu di Atas: Aktif",
        "log_ontop_off": "Selalu di Atas: Mati",
        "log_scan_on": "Pemindaian: Aktif (Mode Dinamis)",
        "log_scan_off": "Pemindaian: Dihentikan",
        "log_err_img": "EROR: File gambar tidak ditemukan!",
        "log_focus": "Game Difokuskan:",
        "log_match": "MATCH: Party Accept!",
        "log_wait": "Diterima. Tunggu",
        "log_lost": "Standby: Fokus jendela hilang (Alt-Tab)",
        "log_saved": "Pengaturan berhasil disimpan.",
        "set_title": "Pengaturan Lanjutan",
        "set_lang": "Bahasa / Language:",
        "set_img": "Nama Gambar:",
        "set_cmin": "Jeda Min. (detik):",
        "set_cmax": "Jeda Maks. (detik):",
        "set_sens": "Sensitivitas:",
        "set_esp": "Mode ESP (Tampilkan Area Pindai)",
        "set_snd": "Bunyikan Suara saat Terima (.wav)",
        "set_browse": "Cari Suara",
        "set_apply": "TERAPKAN (APPLY)",
        "set_ok": "OKE (OK)",
        "warn_stop": "Hentikan pemindaian sebelum mengubah pengaturan.",
        "warn_title": "Peringatan",
        "file_title": "Pilih File Suara"
    }

    # Data Bahasa Inggris
    teks_en = {
        "title": "BPSR Auto-Accept Party Tool",
        "header": "BPSR AUTO-ACCEPT PARTY TOOL",
        "start": "START (F9)",
        "stop": "STOP (F10)",
        "ontop": "📌 Top",
        "mini": "🗕 Mini",
        "full": "🗖 Full",
        "log_on": "📝 Log: ON",
        "log_off": "📝 Log: OFF",
        "btn_clear": "🗑️ Clear Log",
        "settings": "⚙️",
        "status_ready": "Status: Ready / Stopped",
        "status_search": "Status: Running (Searching Game)",
        "status_scan": "Status: Running (Dynamic Scan)",
        "status_standby": "Status: Standby (Waiting Focus)",
        "log_ready": "System Ready. Waiting for instructions.",
        "log_ontop_on": "Always on Top: Active",
        "log_ontop_off": "Always on Top: Inactive",
        "log_scan_on": "Scanning: Active (Dynamic Mode)",
        "log_scan_off": "Scanning: Stopped",
        "log_err_img": "ERROR: Image file not found!",
        "log_focus": "Game Focused:",
        "log_match": "MATCH: Party Accept!",
        "log_wait": "Accepted. Waiting",
        "log_lost": "Standby: Window focus lost (Alt-Tab)",
        "log_saved": "Settings saved successfully.",
        "set_title": "Advanced Settings",
        "set_lang": "Bahasa / Language:",
        "set_img": "Image Name:",
        "set_cmin": "Min Delay (sec):",
        "set_cmax": "Max Delay (sec):",
        "set_sens": "Sensitivity:",
        "set_esp": "ESP Mode (Show Scan Area)",
        "set_snd": "Play Sound on Accept (.wav)",
        "set_browse": "Browse Sound",
        "set_apply": "APPLY",
        "set_ok": "OK",
        "warn_stop": "Stop scanning before changing settings.",
        "warn_title": "Warning",
        "file_title": "Select Sound File"
    }

    if not os.path.exists("lang/id.json"):
        with open("lang/id.json", "w", encoding="utf-8") as f:
            json.dump(teks_id, f, indent=4)
            
    if not os.path.exists("lang/en.json"):
        with open("lang/en.json", "w", encoding="utf-8") as f:
            json.dump(teks_en, f, indent=4)

# Panggil pembuat bahasa otomatis sebelum memulai GUI
inisialisasi_folder_bahasa()

# ================= KELAS OVERLAY ESP =================
class ESPOverlay:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("BPSR_ESP")
        self.root.attributes("-transparentcolor", "black") 
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True) 
        
        w, h = pyautogui.size()
        self.root.geometry(f"{w}x{h}+0+0")
        
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.rect_main = self.canvas.create_rectangle(0,0,0,0, outline="yellow", width=2, dash=(4, 4))
        self.text_main = self.canvas.create_text(0,0, text="AREA", fill="yellow", font=("Consolas", 10, "bold"), anchor="nw")
        
        self.rect_target = self.canvas.create_rectangle(0,0,0,0, outline="#00ff00", width=3)
        self.text_target = self.canvas.create_text(0,0, text="TARGET", fill="#00ff00", font=("Consolas", 10, "bold"), anchor="nw")

        self.root.update_idletasks()
        try:
            hwnd = win32gui.FindWindow(None, "BPSR_ESP")
            styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        except:
            pass

    def update_area(self, x, y, w, h):
        self.canvas.coords(self.rect_main, x, y, x+w, y+h)
        self.canvas.coords(self.text_main, x, max(0, y-18))
        
    def update_target(self, x, y, w, h):
        if w == 0:
            self.canvas.coords(self.rect_target, -100,-100,-100,-100)
            self.canvas.coords(self.text_target, -100,-100)
        else:
            self.canvas.coords(self.rect_target, x, y, x+w, y+h)
            self.canvas.coords(self.text_target, x, max(0, y-18))
            
    def close(self):
        self.root.destroy()

# ================= KELAS GUI UTAMA =================
class BPSR_Precision_GUI:
    def __init__(self, root):
        self.root = root
        
        # Variabel Bahasa Dinamis
        self.daftar_bahasa = []
        self.lang = "id"
        self.translations = {}
        
        self.muat_daftar_bahasa()
        self.muat_bahasa() 
        
        self.root.geometry("440x580")
        self.root.configure(bg="#121212")

        # --- IKON  ---
        try:
            self.root.iconbitmap("bpsr_icon.ico")
        except Exception:
            pass # Abaikan jika file ikon tidak ada
        
        self.colors = {
            "bg": "#121212", "surface": "#1e1e1e", "text": "#e0e0e0",
            "accent": "#3498db", "green": "#218838", "red": "#c82333",
            "border": "#333333", "log_bg": "#000000", "log_fg": "#00ff41",
            "standby": "#f39c12" 
        }
        
        self.sedang_berjalan = False
        self.selalu_di_atas = False
        self.log_terlihat = True
        self.mode_mini = False
        self.status_fokus_terakhir = None
        
        # Variabel ESP & Area Dinamis
        self.esp_window = None
        self.esp_box = None
        self.esp_target = None
        
        self.file_konfigurasi = "setting.cfg" 
        self.muat_konfigurasi()

        self.setup_antarmuka()
        self.mulai_pendengar_tombol_cepat()
        self.root.protocol("WM_DELETE_WINDOW", self.saat_ditutup)
        
        self.root.after(100, self.update_esp_ui)

    def muat_daftar_bahasa(self):
        """Mendeteksi semua file .json di folder lang secara dinamis"""
        self.daftar_bahasa = []
        if os.path.exists("lang"):
            for file in os.listdir("lang"):
                if file.endswith(".json"):
                    self.daftar_bahasa.append(file.replace(".json", ""))
        
        # Jaga-jaga jika folder kosong
        if not self.daftar_bahasa:
            self.daftar_bahasa = ["id"]

    def muat_bahasa(self):
        file_lang = f"lang/{self.lang}.json"
        try:
            with open(file_lang, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception as e:
            self.translations = {}

    def t(self, key):
        return self.translations.get(key, key)

    def muat_konfigurasi(self):
        self.konfigurasi = {
            "file_gambar": "party_request.png",
            "jeda_min": 2.0,
            "jeda_maks": 6.0,
            "tingkat_kecocokan": 0.7,
            "jendela_target": "Blue Protocol: Star Resonance",
            "nama_proses": "StarSEA_Steam.exe",
            "putar_suara": False,
            "mode_esp": False,
            "file_suara": "",
            "bahasa": "id"
        }
        self.parser = configparser.ConfigParser()
        if os.path.exists(self.file_konfigurasi):
            try:
                self.parser.read(self.file_konfigurasi)
                if 'PENGATURAN' in self.parser:
                    set_cfg = self.parser['PENGATURAN']
                    self.konfigurasi["file_gambar"] = set_cfg.get('file_gambar', self.konfigurasi["file_gambar"])
                    self.konfigurasi["jeda_min"] = set_cfg.getfloat('jeda_min', self.konfigurasi["jeda_min"])
                    self.konfigurasi["jeda_maks"] = set_cfg.getfloat('jeda_maks', self.konfigurasi["jeda_maks"])
                    self.konfigurasi["tingkat_kecocokan"] = set_cfg.getfloat('tingkat_kecocokan', self.konfigurasi["tingkat_kecocokan"])
                    self.konfigurasi["putar_suara"] = set_cfg.getboolean('putar_suara', self.konfigurasi["putar_suara"])
                    self.konfigurasi["mode_esp"] = set_cfg.getboolean('mode_esp', self.konfigurasi["mode_esp"])
                    self.konfigurasi["file_suara"] = set_cfg.get('file_suara', self.konfigurasi["file_suara"])
                    
                    bahasa_tersimpan = set_cfg.get('bahasa', self.konfigurasi["bahasa"])
                    # Validasi apakah bahasa masih ada di folder lang/
                    if bahasa_tersimpan in self.daftar_bahasa:
                        self.konfigurasi["bahasa"] = bahasa_tersimpan
                    
                    self.lang = self.konfigurasi["bahasa"]
                    self.muat_bahasa() 
            except Exception:
                pass 

    def simpan_konfigurasi(self):
        try:
            self.parser['PENGATURAN'] = {
                "file_gambar": str(self.konfigurasi["file_gambar"]),
                "jeda_min": str(self.konfigurasi["jeda_min"]),
                "jeda_maks": str(self.konfigurasi["jeda_maks"]),
                "tingkat_kecocokan": str(self.konfigurasi["tingkat_kecocokan"]),
                "putar_suara": str(self.konfigurasi["putar_suara"]),
                "mode_esp": str(self.konfigurasi["mode_esp"]),
                "file_suara": str(self.konfigurasi["file_suara"]),
                "bahasa": str(self.konfigurasi["bahasa"])
            }
            with open(self.file_konfigurasi, "w") as f:
                self.parser.write(f)
        except Exception as e:
            self.tambah_log(f"Gagal menyimpan config: {e}")

    def setup_antarmuka(self):
        self.root.title(self.t("title"))
        self.root.columnconfigure(0, weight=1)

        self.label_header = tk.Label(self.root, text=self.t("header"), font=("Segoe UI", 14, "bold"), 
                                     bg=self.colors["bg"], fg=self.colors["text"])
        self.label_header.grid(row=0, column=0, pady=15)

        self.tombol_pengaturan = tk.Button(self.root, text=self.t("settings"), bg=self.colors["bg"], fg=self.colors["text"], command=self.buka_pengaturan, font=("Segoe UI", 14), bd=0, activebackground=self.colors["bg"], activeforeground=self.colors["accent"], cursor="hand2")
        self.tombol_pengaturan.place(relx=0.96, y=10, anchor="ne")

        self.frame_kontrol = tk.Frame(self.root, bg=self.colors["surface"], padx=10, pady=10, highlightbackground=self.colors["border"], highlightthickness=1)
        self.frame_kontrol.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.frame_kontrol.columnconfigure((0, 1), weight=1)

        self.tombol_mulai = tk.Button(self.frame_kontrol, text=self.t("start"), bg=self.colors["green"], fg="white", font=("Segoe UI", 9, "bold"), bd=0, height=2, command=self.mulai_pindai)
        self.tombol_mulai.grid(row=0, column=0, padx=4, sticky="ew")

        self.tombol_berhenti = tk.Button(self.frame_kontrol, text=self.t("stop"), bg="#424242", fg="#757575", font=("Segoe UI", 9, "bold"), bd=0, height=2, state=tk.DISABLED, command=self.hentikan_pindai)
        self.tombol_berhenti.grid(row=0, column=1, padx=4, sticky="ew")

        self.frame_utilitas = tk.Frame(self.root, bg=self.colors["bg"])
        self.frame_utilitas.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.frame_utilitas.columnconfigure((0, 1, 2, 3), weight=1) 

        self.tombol_di_atas = tk.Button(self.frame_utilitas, text=self.t("ontop"), bg=self.colors["surface"], fg=self.colors["text"], command=self.ubah_selalu_di_atas, font=("Segoe UI", 8))
        self.tombol_di_atas.grid(row=0, column=0, padx=2, sticky="ew")

        self.tombol_mini = tk.Button(self.frame_utilitas, text=self.t("mini"), bg=self.colors["surface"], fg=self.colors["text"], command=self.ubah_mode_mini, font=("Segoe UI", 8))
        self.tombol_mini.grid(row=0, column=1, padx=2, sticky="ew")

        self.tombol_log = tk.Button(self.frame_utilitas, text=self.t("log_on"), bg=self.colors["surface"], fg=self.colors["text"], command=self.ubah_log, font=("Segoe UI", 8))
        self.tombol_log.grid(row=0, column=2, padx=2, sticky="ew")

        self.tombol_hapus_log = tk.Button(self.frame_utilitas, text=self.t("btn_clear"), bg=self.colors["surface"], fg=self.colors["text"], command=self.hapus_log, font=("Segoe UI", 8))
        self.tombol_hapus_log.grid(row=0, column=3, padx=2, sticky="ew")

        self.wadah_log = tk.Frame(self.root, bg=self.colors["bg"])
        self.wadah_log.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")
        self.root.rowconfigure(3, weight=1)

        self.widget_log = scrolledtext.ScrolledText(self.wadah_log, font=("Consolas", 9), bg=self.colors["log_bg"], fg=self.colors["log_fg"], insertbackground="white", bd=0, height=10)
        self.widget_log.pack(fill="both", expand=True)

        self.frame_status = tk.Frame(self.root, bg="#0a0a0a")
        self.frame_status.grid(row=4, column=0, sticky="ew")
        
        self.indikator_status = tk.Label(self.frame_status, text="●", bg="#0a0a0a", fg=self.colors["red"], font=("Segoe UI", 10))
        self.indikator_status.pack(side=tk.LEFT, padx=(10, 0))

        self.var_status = tk.StringVar(value=self.t("status_ready"))
        self.bar_status = tk.Label(self.frame_status, textvariable=self.var_status, bg="#0a0a0a", fg="#7f8c8d", anchor="w", font=("Segoe UI", 8))
        self.bar_status.pack(side=tk.LEFT, padx=(5, 10), pady=2)

        self.tambah_log(self.t("log_ready"))
        
        # Angkat tombol setting ke lapisan teratas agar tidak tertutup frame lain
        self.tombol_pengaturan.lift()


    def perbarui_teks_ui(self):
        self.root.title(self.t("title"))
        self.label_header.config(text=self.t("header"))
        
        if not self.mode_mini:
            self.tombol_mulai.config(text=self.t("start"))
            self.tombol_berhenti.config(text=self.t("stop"))
            self.tombol_mini.config(text=self.t("mini"))
            self.tombol_di_atas.config(text=self.t("ontop"))
            self.tombol_log.config(text=self.t("log_on") if self.log_terlihat else self.t("log_off"))
            self.tombol_hapus_log.config(text=self.t("btn_clear"))
            self.tombol_pengaturan.config(text=self.t("settings"))
        self.var_status.set(self.t("status_ready"))

    def buka_pengaturan(self):
        if self.sedang_berjalan:
            messagebox.showwarning(self.t("warn_title"), self.t("warn_stop"))
            return

        # Muat ulang bahasa secara dinamis jika pengguna menambahkan file json baru selagi aplikasi hidup
        self.muat_daftar_bahasa()

        jendela_pengaturan = tk.Toplevel(self.root)
        jendela_pengaturan.title(self.t("set_title"))
        jendela_pengaturan.geometry("380x400") 
        jendela_pengaturan.configure(bg=self.colors["bg"])
        jendela_pengaturan.resizable(False, False)

        # --- IKON ---
        try:
            jendela_pengaturan.iconbitmap("bpsr_icon.ico")
        except Exception:
            pass
        
        jendela_pengaturan.transient(self.root)
        jendela_pengaturan.grab_set()
        jendela_pengaturan.focus_set()
        
        opsi_slider = {"bg": self.colors["bg"], "fg": self.colors["text"], "troughcolor": self.colors["surface"], "highlightthickness": 0, "orient": tk.HORIZONTAL}

        # --- Dropdown Bahasa Dinamis ---
        lbl_lang = tk.Label(jendela_pengaturan, text=self.t("set_lang"), bg=self.colors["bg"], fg=self.colors["text"])
        lbl_lang.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=10)
        
        var_bahasa = tk.StringVar(value=self.lang)
        opsi_bahasa = tk.OptionMenu(jendela_pengaturan, var_bahasa, *self.daftar_bahasa)
        opsi_bahasa.config(bg=self.colors["surface"], fg="white", highlightthickness=0)
        opsi_bahasa.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="ew")

        lbl_img = tk.Label(jendela_pengaturan, text=self.t("set_img"), bg=self.colors["bg"], fg=self.colors["text"])
        lbl_img.grid(row=1, column=0, sticky="w", pady=5, padx=10)
        
        input_gambar = tk.Entry(jendela_pengaturan, bg=self.colors["surface"], fg="white", bd=1, insertbackground="white")
        input_gambar.insert(0, self.konfigurasi["file_gambar"])
        input_gambar.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        lbl_cmin = tk.Label(jendela_pengaturan, text=self.t("set_cmin"), bg=self.colors["bg"], fg=self.colors["text"])
        lbl_cmin.grid(row=2, column=0, sticky="w", padx=10)
        
        slider_jeda_min = tk.Scale(jendela_pengaturan, from_=1.0, to=15.0, resolution=0.5, **opsi_slider)
        slider_jeda_min.set(self.konfigurasi["jeda_min"])
        slider_jeda_min.grid(row=2, column=1, sticky="ew", padx=10)

        lbl_cmax = tk.Label(jendela_pengaturan, text=self.t("set_cmax"), bg=self.colors["bg"], fg=self.colors["text"])
        lbl_cmax.grid(row=3, column=0, sticky="w", padx=10)
        
        slider_jeda_maks = tk.Scale(jendela_pengaturan, from_=1.0, to=15.0, resolution=0.5, **opsi_slider)
        slider_jeda_maks.set(self.konfigurasi["jeda_maks"])
        slider_jeda_maks.grid(row=3, column=1, sticky="ew", padx=10)

        lbl_sens = tk.Label(jendela_pengaturan, text=self.t("set_sens"), bg=self.colors["bg"], fg=self.colors["text"])
        lbl_sens.grid(row=4, column=0, sticky="w", padx=10)
        
        slider_kecocokan = tk.Scale(jendela_pengaturan, from_=0.4, to=1.0, resolution=0.05, **opsi_slider)
        slider_kecocokan.set(self.konfigurasi["tingkat_kecocokan"])
        slider_kecocokan.grid(row=4, column=1, sticky="ew", padx=10)
        
        var_esp = tk.BooleanVar(value=self.konfigurasi["mode_esp"])
        centang_esp = tk.Checkbutton(jendela_pengaturan, text=self.t("set_esp"), variable=var_esp, bg=self.colors["bg"], fg=self.colors["accent"], selectcolor=self.colors["surface"], activebackground=self.colors["bg"])
        centang_esp.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(5,0))

        var_suara = tk.BooleanVar(value=self.konfigurasi["putar_suara"])
        centang_suara = tk.Checkbutton(jendela_pengaturan, text=self.t("set_snd"), variable=var_suara, bg=self.colors["bg"], fg=self.colors["accent"], selectcolor=self.colors["surface"], activebackground=self.colors["bg"])
        centang_suara.grid(row=6, column=0, columnspan=2, sticky="w", padx=10)

        frame_suara = tk.Frame(jendela_pengaturan, bg=self.colors["bg"])
        frame_suara.grid(row=7, column=0, columnspan=2, sticky="w", padx=30, pady=(0, 10))

        input_suara = tk.Entry(frame_suara, bg=self.colors["surface"], fg="white", bd=1, insertbackground="white", width=25)
        input_suara.insert(0, self.konfigurasi.get("file_suara", ""))
        input_suara.pack(side=tk.LEFT, padx=(0, 5))

        def cari_suara():
            file = filedialog.askopenfilename(title=self.t("file_title"), filetypes=[("Audio WAV", "*.wav")])
            if file:
                input_suara.delete(0, tk.END)
                input_suara.insert(0, file)

        tombol_cari = tk.Button(frame_suara, text=self.t("set_browse"), bg=self.colors["surface"], fg=self.colors["text"], command=cari_suara)
        tombol_cari.pack(side=tk.LEFT)

        def simpan_dan_terapkan(tutup_jendela=False):
            jeda_minimum = slider_jeda_min.get()
            jeda_maksimum = slider_jeda_maks.get()
            if jeda_minimum > jeda_maksimum: jeda_maksimum = jeda_minimum

            bahasa_baru = var_bahasa.get()
            ganti_bahasa = self.lang != bahasa_baru

            self.konfigurasi.update({
                "file_gambar": input_gambar.get().strip(),
                "jeda_min": jeda_minimum,
                "jeda_maks": jeda_maksimum,
                "tingkat_kecocokan": slider_kecocokan.get(),
                "putar_suara": var_suara.get(),
                "mode_esp": var_esp.get(),
                "file_suara": input_suara.get().strip(),
                "bahasa": bahasa_baru
            })
            
            self.simpan_konfigurasi()
            
            if ganti_bahasa:
                self.lang = bahasa_baru
                self.muat_bahasa()
                self.perbarui_teks_ui()

            self.tambah_log(self.t("log_saved"))
            
            if tutup_jendela:
                jendela_pengaturan.destroy()

        frame_aksi = tk.Frame(jendela_pengaturan, bg=self.colors["bg"])
        frame_aksi.grid(row=8, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        frame_aksi.columnconfigure((0, 1), weight=1)

        tombol_apply = tk.Button(frame_aksi, text=self.t("set_apply"), bg=self.colors["surface"], fg="white", bd=1, height=2, command=lambda: simpan_dan_terapkan(False))
        tombol_apply.grid(row=0, column=0, padx=5, sticky="ew")

        tombol_ok = tk.Button(frame_aksi, text=self.t("set_ok"), bg=self.colors["accent"], fg="white", bd=0, height=2, command=lambda: simpan_dan_terapkan(True))
        tombol_ok.grid(row=0, column=1, padx=5, sticky="ew")

    # ================= LOGIKA ESP & GUI =================
    def update_esp_ui(self):
        if self.konfigurasi["mode_esp"] and self.sedang_berjalan and self.status_fokus_terakhir == "Focused":
            if not self.esp_window:
                self.esp_window = ESPOverlay()
            
            if self.esp_box:
                self.esp_window.update_area(*self.esp_box)
            if self.esp_target:
                self.esp_window.update_target(*self.esp_target)
            else:
                self.esp_window.update_target(0,0,0,0)
        else:
            if self.esp_window:
                self.esp_window.close()
                self.esp_window = None
                
        self.root.after(50, self.update_esp_ui)

    def hapus_log(self):
        self.widget_log.config(state=tk.NORMAL)
        self.widget_log.delete(1.0, tk.END)
        self.widget_log.config(state=tk.DISABLED)

    def tambah_log(self, pesan):
        def tulis_log():
            sekarang = datetime.now().strftime("%H:%M:%S")
            self.widget_log.config(state=tk.NORMAL)
            self.widget_log.insert(tk.END, f"[{sekarang}] {pesan}\n")
            self.widget_log.see(tk.END)
            self.widget_log.config(state=tk.DISABLED)
        self.root.after(0, tulis_log)

    def ubah_log(self):
        if self.log_terlihat:
            self.wadah_log.grid_remove()
            if not self.mode_mini:
                self.tombol_log.config(text=self.t("log_off"))
                self.root.geometry("440x280")
        else:
            self.wadah_log.grid()
            if not self.mode_mini:
                self.tombol_log.config(text=self.t("log_on"))
                self.root.geometry("440x580")
        self.log_terlihat = not self.log_terlihat

    def ubah_mode_mini(self):
        if not self.mode_mini:
            self.label_header.grid_remove()
            if self.log_terlihat: self.ubah_log()
            
            # 1. Tambah tinggi jadi 160 agar status bar selalu terlihat langsung
            self.root.geometry("350x160") 
            
            # 2. Geser frame kontrol ke bawah sedikit (pady=25) agar ada ruang kosong di atasnya
            self.frame_kontrol.grid(row=1, column=0, padx=20, pady=(25, 5), sticky="ew")
            
            # 3. Taruh ikon setting di area kosong kanan atas. relx=0.97 akan membuatnya 
            #    otomatis bergeser mengikuti panjang jendela ketika di-drag.
            self.tombol_pengaturan.place(relx=0.97, y=5, anchor="ne")
            self.tombol_pengaturan.lift()
            
            self.tombol_mulai.config(text="▶", font=("Segoe UI", 12), height=1)
            self.tombol_berhenti.config(text="⏹", font=("Segoe UI", 12), height=1)
            
            self.tombol_di_atas.config(text="📌", font=("Segoe UI", 10))
            self.tombol_mini.config(text="🗖", bg=self.colors["accent"], font=("Segoe UI", 10))
            self.tombol_log.config(text="📝", font=("Segoe UI", 10))
            self.tombol_hapus_log.config(text="🗑️", font=("Segoe UI", 10))
            
            self.mode_mini = True
        else:
            self.label_header.grid()
            self.root.geometry("440x580")
            
            if not self.log_terlihat: self.ubah_log()
            
            # Kembalikan posisi frame kontrol ke asal
            self.frame_kontrol.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
            
            # Kembalikan posisi icon setting ke mode penuh
            self.tombol_pengaturan.place(relx=0.96, y=10, anchor="ne")
            self.tombol_pengaturan.lift()
            
            self.tombol_mulai.config(text=self.t("start"), font=("Segoe UI", 9, "bold"), height=2)
            self.tombol_berhenti.config(text=self.t("stop"), font=("Segoe UI", 9, "bold"), height=2)
            
            self.tombol_di_atas.config(text=self.t("ontop"), font=("Segoe UI", 8))
            self.tombol_mini.config(text=self.t("mini"), bg=self.colors["surface"], font=("Segoe UI", 8))
            self.tombol_log.config(text=self.t("log_on") if self.log_terlihat else self.t("log_off"), font=("Segoe UI", 8))
            self.tombol_hapus_log.config(text=self.t("btn_clear"), font=("Segoe UI", 8))
            
            self.mode_mini = False

    def ubah_selalu_di_atas(self):
        self.selalu_di_atas = not self.selalu_di_atas
        self.root.attributes("-topmost", self.selalu_di_atas)
        self.tombol_di_atas.config(bg=self.colors["accent"] if self.selalu_di_atas else self.colors["surface"])
        self.tambah_log(self.t("log_ontop_on") if self.selalu_di_atas else self.t("log_ontop_off"))

    # ================= SISTEM PENCARIAN WINDOW DINAMIS YANG LEBIH AKURAT =================
    def dapatkan_area_game(self):
        """Mencari jendela game dan mengembalikan koordinat area dalam (Client Area) di layar."""
        hwnd_target = 0
        
        # Fungsi callback untuk mencari judul window
        def callback(hwnd, extra):
            nonlocal hwnd_target
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if self.konfigurasi["jendela_target"] in title:
                    hwnd_target = hwnd
                    return False # Berhenti mencari
            return True
        
        try:
            win32gui.EnumWindows(callback, None)
        except Exception:
            pass
            
        if hwnd_target:
            # Dapatkan Client Rect (area murni dalam game tanpa bingkai/title bar)
            client_rect = win32gui.GetClientRect(hwnd_target)
            
            # Konversi titik (0,0) dari client area ke koordinat layar sebenarnya (Screen Coordinates)
            left_top = win32gui.ClientToScreen(hwnd_target, (0, 0))
            
            x = left_top[0]
            y = left_top[1]
            w = client_rect[2]
            h = client_rect[3]
            
            # Validasi agar tidak merekam saat gamenya di-minimize (biasanya koordinat minus sangat jauh)
            if x > -30000 and y > -30000 and w > 0 and h > 0:
                return {"left": x, "top": y, "width": w, "height": h}
                
        return None

    def mulai_pindai(self):
        if not self.sedang_berjalan:
            if not os.path.exists(self.konfigurasi["file_gambar"]):
                self.tambah_log(self.t("log_err_img"))
                return
            self.sedang_berjalan = True
            self.status_fokus_terakhir = None
            self.tombol_mulai.config(state=tk.DISABLED, bg="#424242")
            self.tombol_berhenti.config(state=tk.NORMAL, bg=self.colors["red"], fg="white")
            
            self.indikator_status.config(fg=self.colors["green"])
            self.var_status.set("Status: Running")
            
            self.esp_box = None
            self.esp_target = None
            
            threading.Thread(target=self.siklus_pindai, daemon=True).start()
            self.tambah_log(self.t("log_scan_on"))

    def hentikan_pindai(self):
        if self.sedang_berjalan:
            self.sedang_berjalan = False
            self.tombol_mulai.config(state=tk.NORMAL, bg=self.colors["green"])
            self.tombol_berhenti.config(state=tk.DISABLED, bg="#424242", fg="#757575")
            
            self.indikator_status.config(fg=self.colors["red"])
            self.var_status.set(self.t("status_ready"))
            self.esp_target = None
            self.esp_box = None
            
            self.tambah_log(self.t("log_scan_off"))

    # ================= LOGIKA PEMINDAIAN MSS & OPENCV (DINAMIS & AUTO-SCALE) =================
    def siklus_pindai(self):
        try:
            # 1. Muat template asli (Dari resolusi 1920x1080)
            original_template = cv2.imread(self.konfigurasi["file_gambar"], cv2.IMREAD_GRAYSCALE)
            
            # Resolusi saat gambar di-crop (Biarkan 1920x1080)
            base_res_w = 1920
            base_res_h = 1080
            
            # Cache untuk menyimpan template yang sudah di-resize agar performa tetap ringan
            current_template = original_template.copy()
            template_h, template_w = current_template.shape
            
            # Variabel untuk melacak ukuran window
            last_game_w = 0
            last_game_h = 0
            
        except Exception as e:
            self.tambah_log(f"Gagal memuat template: {e}")
            self.hentikan_pindai()
            return

        with mss.mss() as sct:
            while self.sedang_berjalan:
                try:
                    active_win = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    
                    if self.konfigurasi["jendela_target"] in active_win:
                        area_game = self.dapatkan_area_game()
                        
                        if area_game:
                            # --- FITUR AUTO-SCALE TEMPLATE ---
                            game_w = area_game["width"]
                            game_h = area_game["height"]
                            
                            # Jika ukuran window game berubah (misal dari Fullscreen ke Windowed)
                            if game_w != last_game_w or game_h != last_game_h:
                                # Hitung rasio pengecilan/pembesaran
                                scale_w = game_w / base_res_w
                                scale_h = game_h / base_res_h
                                scale = min(scale_w, scale_h) # Gunakan skala terkecil agar proporsional
                                
                                new_w = int(original_template.shape[1] * scale)
                                new_h = int(original_template.shape[0] * scale)
                                
                                # Cegah error gambar menjadi terlalu kecil
                                if new_w > 10 and new_h > 10:
                                    # Ubah ukuran template secara dinamis!
                                    current_template = cv2.resize(original_template, (new_w, new_h), interpolation=cv2.INTER_AREA)
                                    template_h, template_w = current_template.shape
                                    self.tambah_log(f"Skala disesuaikan: {new_w}x{new_h} (Game: {game_w}x{game_h})")
                                
                                last_game_w = game_w
                                last_game_h = game_h
                            # ---------------------------------

                            if self.status_fokus_terakhir != "Focused":
                                self.tambah_log(f"Game Terdeteksi: {self.konfigurasi['nama_proses']}")
                                self.indikator_status.config(fg=self.colors["green"])
                                self.var_status.set(self.t("status_scan"))
                                self.status_fokus_terakhir = "Focused"

                            # Kotak kuning ESP
                            self.esp_box = (area_game["left"], area_game["top"], area_game["width"], area_game["height"])

                            img_sct = np.array(sct.grab(area_game))
                            img_gray = cv2.cvtColor(img_sct, cv2.COLOR_BGRA2GRAY)
                            
                            # Pencocokan gambar (Menggunakan current_template yang sudah di-resize otomatis!)
                            res = cv2.matchTemplate(img_gray, current_template, cv2.TM_CCOEFF_NORMED)
                            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                            
                            if max_val >= self.konfigurasi["tingkat_kecocokan"]:
                                match_x = max_loc[0] + area_game["left"]
                                match_y = max_loc[1] + area_game["top"]
                                
                                self.esp_target = (match_x, match_y, template_w, template_h)
                                
                                self.tambah_log(self.t("log_match"))
                                pydirectinput.press(';') 
                                
                                if self.konfigurasi["putar_suara"]:
                                    jalur_suara = self.konfigurasi.get("file_suara", "")
                                    if jalur_suara and os.path.exists(jalur_suara):
                                        winsound.PlaySound(jalur_suara, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                        
                                delay = random.uniform(self.konfigurasi["jeda_min"], self.konfigurasi["jeda_maks"])
                                self.tambah_log(f"{self.t('log_wait')} {delay:.1f}s")
                                
                                time.sleep(delay)
                                self.esp_target = None 
                        else:
                            time.sleep(0.5)
                    else:
                        if self.status_fokus_terakhir != "Standby":
                            self.tambah_log(self.t("log_lost"))
                            self.indikator_status.config(fg=self.colors["standby"]) 
                            self.var_status.set(self.t("status_standby"))
                            self.status_fokus_terakhir = "Standby"
                            self.esp_box = None 
                    
                    time.sleep(0.5) 
                except Exception as e:
                    time.sleep(1)

    def mulai_pendengar_tombol_cepat(self):
        def periksa_tombol():
            while True:
                if keyboard.is_pressed('f9'): self.root.after(0, self.mulai_pindai)
                if keyboard.is_pressed('f10'): self.root.after(0, self.hentikan_pindai)
                if keyboard.is_pressed('f11'): self.root.after(0, self.ubah_selalu_di_atas)
                time.sleep(0.1)
        threading.Thread(target=periksa_tombol, daemon=True).start()

    def saat_ditutup(self):
        self.sedang_berjalan = False
        if self.esp_window:
            self.esp_window.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = BPSR_Precision_GUI(root)
    root.mainloop()