# Dubplate Collector

A minimalistic console-based tool for maintaining a personal dubplate database.  
Designed for DJs and collectors who store exclusive or rare dubplates and want a fast, local, and organized way to manage their library.

This project uses SQLite as a lightweight local database and provides simple, menu-driven navigation entirely from the terminal.

---

## 🎧 Features

- Add, delete, and search tracks  
- Import tracklists from two formats:
  - `Artist - Title.ext`
  - Export-style format: `Artist – Title [EXT]`
- Export your full dubplate catalog to a TXT file
- Duplicate protection
- Clean, readable console interface

---

## 📂 Track Structure

Each entry in the database contains:

| Field     | Description                         |
|-----------|-------------------------------------|
| Artist    | Name of the artist (optional)       |
| Title     | Track title                         |
| Filetype  | mp3 / wav / flac / aiff             |

---

## 📦 Building an EXE

1. Install PyInstaller:
pip install pyinstaller

2. Build executable:
pyinstaller --onefile "./Dubplate Collector.py"

The resulting EXE will appear in: dist/dubplates.exe


