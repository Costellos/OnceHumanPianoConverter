# 🎹 Once Human Piano Converter

Convert piano melodies into Once Human in-game keypress format (`Shift + T`, `Ctrl + Q`, etc.), with support for:
- ✅ MIDI file parsing
- ✅ Manual note entry
- ✅ Beat timing and rhythm
- ✅ Auto-looping
- ✅ Modifier-aware key mapping
- ✅ Output to text for practice
- ✅ Output to MIDI for validation

---

## 🛠 Requirements

- Python 3.8+
- Install required packages:

```bash
pip install mido python-rtmidi
```

---

## 📂 Folder Structure

```
once_human_piano_converter/
├── midi_samples/               # Place your .mid files here
├── output/                     # Converted practice files
├── validation_output/          # Rebuilt MIDI files for validation
├── oncehuman_converter.py      # Main converter tool
├── validate_output_to_midi.py  # Tool to convert text output back to MIDI
└── README.md
```

---

## 🚀 How to Use

### 🔁 Run the converter:

```bash
python oncehuman_converter.py
```

### 💡 Menu options:

1. **Convert MIDI file**
   - Parses `.mid`, extracts melody + rhythm
2. **Manual note input**
   - Example format: `C4:1.0 D#4:0.5 E4`
3. **Show key map**
   - View in-game keyboard layout

---

## ⚙️ Flags (Optional)

Use these flags when running the script to control behavior:

| Flag         | Description                                         |
|--------------|-----------------------------------------------------|
| `--strict`   | Rejects notes outside octaves 3–5                  |
| `--clip`     | Automatically rounds out-of-range notes to 3–5     |

🎵 Only use one flag at a time.  
🚫 Without flags, out-of-range notes are allowed but unmodified.

---

## 🎧 Validate with MIDI

To rebuild MIDI files from your converted practice files:

```bash
python validate_output_to_midi.py
```

You'll be prompted to enter a path like:

```
output/my_song.txt
```

It will generate:

```
validation_output/validation_my_song.mid
```

✅ Use any MIDI viewer or player (e.g. MuseScore, VLC) to test output.

---

## 🧠 Notes & Defaults

| Feature           | Default       |
|------------------|----------------|
| Tempo (BPM)       | 60 BPM         |
| Note duration     | `1.0 beat` (if omitted) |
| Octaves used      | 3 (Ctrl), 4 (default), 5 (Shift) |
| Key mappings      | `Q W E R T Y U` (white) + `2 3 5 6 7` (black) |

---

## 📮 Example Practice Output

```
Shift + T
Shift + Q
Shift + W
Q (0.5 beats)
Ctrl + 6
```

---

## 🧑‍💻 Author & License

Developed by Steven Costello for custom piano input in Once Human.

MIT License — use and modify freely.