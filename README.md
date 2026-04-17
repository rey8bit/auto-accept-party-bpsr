# BPSR Auto-Accept Party Tool (experimental)

[Bahasa Indonesia](README_id.md) / **English**

A lightweight automation tool with a modern interface (**Dark Mode**) for automatically accepting party requests in **Blue Protocol: Star Resonance**. 

> **Note:** Optimized for the Steam client (`StarSEA_Steam.exe`). Use at your own risk.

This tool is designed to make it easier for players to automatically accept party requests while focused on the game screen, using efficient image detection.

### How to use
1. After compile the code to executeable (or just simply run the python code on specific folder, if you know to do), don't forget to add the image to detect, like "party_apply.png" on same folder.
2. Run the code or app as usual.

### 📸 Interface Preview
| Full Mode (Active) | Mini Mode | Detected |
|---|---|---|
| ![Full UI](app2.png) | ![Mini Mode](appmini.png) | ![Player Detected Screenshot](appdetected.png) |

Some of pictures was taken on previous build, but still same function.

### ✨ Key Features
- **Full Dark Mode**: "Midnight Stealth" dark theme, easy on the eyes for long gaming sessions.
- **Modular UI**: Switch to **Mini Mode** for an ultra-compact view in the corner of your screen.
- **Log Toggle**: Show or hide the detection activity log as needed.
- **Focus Awareness**: The script only scans the screen when the game window (`StarSEA_Steam.exe`) is active. It automatically enters **Standby** mode when you Alt-Tab.
- **Top Toggle**: "**Top**" button to keep the application window floating over the game window.
- **Performance Optimization**: Low CPU usage through adaptive scanning logic.

### 🛠️ Installation & Build Guide
1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Download this repository and open a terminal/CMD in the project folder.
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
