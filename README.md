# BPSR Auto-Accept Party Tool

[Bahasa Indonesia](README_id.md) / **English**

A lightweight, open-source automation tool to automatically accept party invites in **Blue Protocol: Star Resonance**.

### ✨ Features
- **Auto-Scale**: Works on any resolution (1080p, 900p, 720p, etc.) without extra setup.
- **ESP Overlay**: Visual boxes to track scanning area and targets.
- **MSS + OpenCV**: Fast detection with very low CPU usage.
- **Multi-Language**: Easy translation via JSON files in the `lang/` folder.
- **Mini Mode**: Compact UI to save screen space.

### ⌨️ Hotkeys
- **F9**: Start Scanning
- **F10**: Stop Scanning
- **F11**: Toggle Always-on-Top

### 🛠️ Installation & How to Use
Since this tool is distributed as source code for transparency, you need Python to run or compile it:
1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Clone/download this repository.
3. Install the required dependencies by running: `pip install -r requirements.txt`
4. Place your target image (example: `party_request.png`) in the application folder.
Example: This cropped image was taken at 1080p resolution.
![Example](party_request_1080.png)
5. Run the script via terminal: `python bpsr_auto_accept_gui.py` (or compile it yourself using PyInstaller).
6. Press **F9** or click play to run the app.

---
*Optimized for `StarSEA_Steam.exe`, but you can change for standalone client by editing the script. Use at your own risk.*
