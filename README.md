# 🖥️ OCR Snipping Tool (Windows)

A lightweight Windows screen snipping tool that lets you select any area of your screen and instantly copy the detected text to your clipboard using OCR (Tesseract).

---

## ✨ Features

- 📸 Drag-to-select screen area (like Windows Snipping Tool)
- 🧠 OCR text recognition using Tesseract
- 📋 Auto-copy result to clipboard
- ⚡ Fast preprocessing for better accuracy
- 🪟 Works as a standalone Windows EXE (no Python needed)

---

## 🚀 Running the App (Python)

### 1. Install dependencies

```bash
pip install -r requirements.txt


2. Install Tesseract OCR

Download and install:

👉 https://github.com/UB-Mannheim/tesseract/wiki

Default path should be:

C:\Program Files\Tesseract-OCR\
3. Run the app
python ocrWin.py
🧱 Building the EXE (IMPORTANT)

This project is designed to be packaged into a standalone Windows executable.

1. Install PyInstaller
pip install pyinstaller
2. Ensure project structure

Your project should look like this:

ocrWin/
│
├── ocrWin.py
├── requirements.txt
├── tesseract/
│   ├── tesseract.exe
│   ├── *.dll files
│   └── tessdata/
│       ├── eng.traineddata
│       ├── pol.traineddata (optional)
│
├── .gitignore
└── README.md
3. Build the EXE

Run this command:

pyinstaller --onefile --windowed \
  --add-data "tesseract;tesseract" \
  --hidden-import=cv2 \
  ocrWin.py
4. Output

Your executable will be created here:

dist/ocrWin.exe

You can now:

Run it without Python installed
Move it to any Windows machine
Bind it to a shortcut key
⌨️ Optional: Add Hotkey Launch

You can assign a Windows shortcut:

Right-click ocrWin.exe
Create shortcut
Right-click shortcut → Properties
Set shortcut key (e.g. Ctrl + Shift + S)
🧠 OCR Accuracy Tips

For better results:

Ensure text is high contrast
Avoid very small fonts (or use scaling in code)
Install language packs:
eng.traineddata
pol.traineddata
⚠️ Notes
Tesseract must be included in tesseract/ folder for EXE builds
Do NOT commit venv/, build/, or dist/ folders
.gitignore is already configured for this
📦 Tech Stack
Python
PyQt5 (UI overlay)
Tesseract OCR
OpenCV (image preprocessing)
PIL / mss (screen capture)
PyInstaller (packaging)
📄 License

Free to use for personal or commercial projects.

🚀 Result

Press shortcut → drag area → text instantly copied to clipboard.
