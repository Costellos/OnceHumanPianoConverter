import mido
from mido import MidiFile
import os
import sys

STRICT_MODE = '--strict' in sys.argv
CLIP_MODE = '--clip' in sys.argv


note_map = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E',
    5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}

key_mapping = {
    'C': 'Q',  'C#': '2',
    'D': 'W',  'D#': '3',
    'E': 'E',
    'F': 'R',  'F#': '5',
    'G': 'T',  'G#': '6',
    'A': 'Y',  'A#': '7',
    'B': 'U'
}

def midi_note_to_string(note_num):
    pitch = note_num % 12
    octave = (note_num // 12) - 1
    return f"{note_map[pitch]}{octave}"

def convert_note(note_str):
    if ':' in note_str:
        note_str, duration = note_str.split(':')
        duration = float(duration)
    else:
        duration = 1.0

    if len(note_str) == 2:
        note, octave = note_str[0], int(note_str[1])
    elif len(note_str) == 3 and note_str[1] == '#':
        note, octave = note_str[:2], int(note_str[2])
    else:
        return f"[Invalid:{note_str}]"

    key = key_mapping.get(note)
    if not key:
        return f"[Unknown:{note_str}]"

    if octave < 3 or octave > 5:
        if STRICT_MODE:
            return f"[Rejected: Octave {octave}]"
        elif CLIP_MODE:
            octave = max(3, min(5, octave))  # clip to 3–5

    modifier = ''
    if octave == 3:
        modifier = 'Ctrl + '
    elif octave == 5:
        modifier = 'Shift + '
    elif octave != 4:
        return f"[Octave:{octave}]"

    if duration == 1.0:
        return f"{modifier}{key}"
    else:
        return f"{modifier}{key} ({duration} beat{'s' if duration != 1.0 else ''})"


def convert_midi_file(filepath):
    midi = MidiFile(filepath)
    ticks_per_beat = midi.ticks_per_beat
    tempo = 50000 # default 120 BPM
    abs_time = 0
    notes = []

    for msg in midi:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
        if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
            abs_time += msg.time
            beats = round(msg.time / ticks_per_beat, 2)
            note = midi_note_to_string(msg.note)
            converted = convert_note(f"{note}:{beats if beats > 0 else 1.0}")
            notes.append((converted, beats if beats > 0 else 1.0))

    return notes, tempo

def save_to_file(filename, sequence, tempo):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w") as f:
        f.write(f"# Tempo: {round(60000000 / tempo)} BPM\n")
        f.write("# Each line is one note with timing in beats\n\n")
        for item, beat in sequence:
            f.write(f"{item}\n")
    print(f"✅ Saved to output/{filename}")

def manual_input():
    user_input = input("Enter notes (e.g. C4:1.0 D#4:0.5 G5): ")
    notes = user_input.strip().split()
    converted = [(convert_note(note), float(note.split(':')[1]) if ':' in note else 1.0) for note in notes]
    return converted, 500000

def show_keyboard_map():
    print("\n🎹 Once Human Keyboard Map:")
    print("White Keys : Q W E R T Y U")
    print("Black Keys : 2 3   5 6 7")
    print("Octaves: Ctrl = Low (3), Default = Mid (4), Shift = High (5)\n")

def main():
    print("🎼 Once Human Piano Converter")
    print("1. Convert MIDI file")
    print("2. Manual note input")
    print("3. Show key map")
    choice = input("> ")

    if choice == "1":
        filepath = input("Path to MIDI file (e.g. midi_samples/example.mid): ")
        if not os.path.exists(filepath):
            print("File not found.")
            return
        notes, tempo = convert_midi_file(filepath)
        save = input("Save to file? (y/n): ")
        if save.lower() == "y":
            filename = input("Enter filename (e.g. zelda_lullaby.txt): ")
            save_to_file(filename, notes, tempo)
    elif choice == "2":
        notes, tempo = manual_input()
        save = input("Save to file? (y/n): ")
        if save.lower() == "y":
            filename = input("Enter filename (e.g. custom_song.txt): ")
            save_to_file(filename, notes, tempo)
    elif choice == "3":
        show_keyboard_map()
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()