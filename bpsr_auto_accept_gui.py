import tkinter as tk
from tkinter import scrolledtext
import threading
import pydirectinput
import keyboard
import pyautogui
import time
import win32gui
import win32con
import random
import os
from datetime import datetime

class BPSR_Precision_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BPSR Auto-Accept Party")
        self.root.geometry("420x550")
        self.root.configure(bg="#121212")
        
        # --- CONFIG COLORS ---
        self.colors = {
            "bg": "#121212", "surface": "#1e1e1e", "text": "#e0e0e0",
            "accent": "#3498db", "green": "#218838", "red": "#c82333",
            "border": "#333333", "log_bg": "#000000", "log_fg": "#00ff41"
        }
        
        # Logic State
        self.is_running = False
        self.is_always_on_top = False
        self.log_visible = True
        self.mini_mode = False
        self.last_focus_state = None 
        
        self.image_file = 'party_apply.png'
        self.target_window = "Blue Protocol: Star Resonance"
        self.process_name = "StarSEA_Steam.exe"

        self.setup_ui()
        self.start_hotkey_listener()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)

        # 1. Header
        self.header_label = tk.Label(self.root, text="BPSR Auto-Accept Party", font=("Segoe UI", 14, "bold"), 
                                     bg=self.colors["bg"], fg=self.colors["text"])
        self.header_label.grid(row=0, column=0, pady=15)

        # 2. Control Frame
        self.ctrl_frame = tk.Frame(self.root, bg=self.colors["surface"], padx=10, pady=10, 
                                   highlightbackground=self.colors["border"], highlightthickness=1)
        self.ctrl_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.ctrl_frame.columnconfigure((0, 1), weight=1)

        self.btn_start = tk.Button(self.ctrl_frame, text="START (F9)", bg=self.colors["green"], fg="white", 
                                   font=("Segoe UI", 9, "bold"), bd=0, height=2, command=self.start_scan)
        self.btn_start.grid(row=0, column=0, padx=4, sticky="ew")

        self.btn_stop = tk.Button(self.ctrl_frame, text="STOP (F10)", bg="#424242", fg="#757575", 
                                  font=("Segoe UI", 9, "bold"), bd=0, height=2, state=tk.DISABLED, command=self.stop_scan)
        self.btn_stop.grid(row=0, column=1, padx=4, sticky="ew")

        # 3. Utility Frame (Top, Mini, Log Toggle)
        self.util_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.util_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.util_frame.columnconfigure((0, 1, 2), weight=1)

        self.btn_ontop = tk.Button(self.util_frame, text="Top", bg=self.colors["surface"], fg=self.colors["text"],
                                   command=self.toggle_always_on_top, font=("Segoe UI", 8))
        self.btn_ontop.grid(row=0, column=0, padx=2, sticky="ew")

        self.btn_mini = tk.Button(self.util_frame, text="MINI", bg=self.colors["surface"], fg=self.colors["text"],
                                  command=self.toggle_mini_mode, font=("Segoe UI", 8))
        self.btn_mini.grid(row=0, column=1, padx=2, sticky="ew")

        self.btn_log_toggle = tk.Button(self.util_frame, text="LOG: ON", bg=self.colors["surface"], fg=self.colors["text"],
                                        command=self.toggle_log, font=("Segoe UI", 8))
        self.btn_log_toggle.grid(row=0, column=2, padx=2, sticky="ew")

        # 4. Log Section
        self.log_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.log_container.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")
        self.root.rowconfigure(3, weight=1)

        self.log_widget = scrolledtext.ScrolledText(self.log_container, font=("Consolas", 9), 
                                                    bg=self.colors["log_bg"], fg=self.colors["log_fg"],
                                                    insertbackground="white", bd=0, height=10)
        self.log_widget.pack(fill="both", expand=True)

        # 5. Status Bar Footer
        self.status_var = tk.StringVar(value="Status: Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#0a0a0a", fg="#7f8c8d", 
                                   anchor="w", padx=10, font=("Segoe UI", 8))
        self.status_bar.grid(row=4, column=0, sticky="ew")

        # Initial System Log
        res = pyautogui.size()
        self.add_log(f"Sistem Siap. Resolusi: {res.width}x{res.height}")

    # ================= UI LOGIC =================

    def add_log(self, message):
        def append():
            now = datetime.now().strftime("%H:%M:%S")
            self.log_widget.config(state=tk.NORMAL)
            self.log_widget.insert(tk.END, f"[{now}] {message}\n")
            self.log_widget.see(tk.END)
            self.log_widget.config(state=tk.DISABLED)
        self.root.after(0, append)

    def toggle_log(self):
        if self.log_visible:
            self.log_container.grid_remove()
            self.btn_log_toggle.config(text="LOG: OFF")
            if not self.mini_mode: self.root.geometry("420x280")
        else:
            self.log_container.grid()
            self.btn_log_toggle.config(text="LOG: ON")
            if not self.mini_mode: self.root.geometry("420x550")
        self.log_visible = not self.log_visible

    def toggle_mini_mode(self):
        if not self.mini_mode:
            self.header_label.grid_remove()
            if self.log_visible: self.toggle_log()
            self.root.geometry("280x160")
            self.btn_mini.config(text="FULL", bg=self.colors["accent"])
            self.mini_mode = True
        else:
            self.header_label.grid()
            self.root.geometry("420x550")
            if not self.log_visible: self.toggle_log()
            self.btn_mini.config(text="MINI", bg=self.colors["surface"])
            self.mini_mode = False

    def toggle_always_on_top(self):
        self.is_always_on_top = not self.is_always_on_top
        self.root.attributes("-topmost", self.is_always_on_top)
        self.btn_ontop.config(bg=self.colors["accent"] if self.is_always_on_top else self.colors["surface"])
        self.add_log(f"Always on Top: {'Aktif' if self.is_always_on_top else 'Mati'}")

    def start_scan(self):
        if not self.is_running:
            if not os.path.exists(self.image_file):
                self.add_log(f"ERROR: {self.image_file} tidak ditemukan!")
                return
            self.is_running = True
            self.last_focus_state = None
            self.btn_start.config(state=tk.DISABLED, bg="#424242")
            self.btn_stop.config(state=tk.NORMAL, bg=self.colors["red"], fg="white")
            self.status_var.set("Status: Running")
            threading.Thread(target=self.scan_loop, daemon=True).start()
            self.add_log("Pemindaian: Aktif")

    def stop_scan(self):
        if self.is_running:
            self.is_running = False
            self.btn_start.config(state=tk.NORMAL, bg=self.colors["green"])
            self.btn_stop.config(state=tk.DISABLED, bg="#424242", fg="#757575")
            self.status_var.set("Status: Stopped")
            self.add_log("Pemindaian: Berhenti")

    def scan_loop(self):
        while self.is_running:
            try:
                # Ambil judul window yang sedang aktif
                active_win = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                
                if self.target_window in active_win:
                    if self.last_focus_state != "Focused":
                        self.add_log(f"Game Terdeteksi: {self.process_name}")
                        self.status_var.set("Status: Running")
                        self.last_focus_state = "Focused"

                    # Scan layar
                    match = pyautogui.locateOnScreen(self.image_file, confidence=0.7, region=(1000, 0, 920, 600))
                    if match:
                        self.add_log("MATCH: Party Accept!")
                        pydirectinput.press(';')
                        delay = random.uniform(4.0, 6.0)
                        self.add_log(f"Diterima. Tunggu {delay:.1f}s")
                        time.sleep(delay)
                else:
                    if self.last_focus_state != "Standby":
                        self.add_log("Standby: Fokus jendela hilang (Alt-Tab)")
                        self.status_var.set("Status: Standby (Alt-Tab)")
                        self.last_focus_state = "Standby"
                
                time.sleep(0.5)
            except Exception as e:
                time.sleep(1)

    def start_hotkey_listener(self):
        def check():
            while True:
                if keyboard.is_pressed('f9'): self.root.after(0, self.start_scan)
                if keyboard.is_pressed('f10'): self.root.after(0, self.stop_scan)
                if keyboard.is_pressed('f11'): self.root.after(0, self.toggle_always_on_top)
                time.sleep(0.1)
        threading.Thread(target=check, daemon=True).start()

    def on_closing(self):
        self.is_running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BPSR_Precision_GUI(root)
    root.mainloop()