import mido
from mido import Message, MidiFile, MidiTrack
import re
import os

# Reverse key mapping
reverse_key_map = {
    'Q': 60,  '2': 61,
    'W': 62,  '3': 63,
    'E': 64,
    'R': 65,  '5': 66,
    'T': 67,  '6': 68,
    'Y': 69,  '7': 70,
    'U': 71
}

def get_octave_modifier(modifier):
    if modifier == 'Ctrl':
        return -1  # Octave 3 = MIDI base 60 - 12
    elif modifier == 'Shift':
        return +1  # Octave 5 = MIDI base 60 + 12
    return 0  # Octave 4

def convert_line_to_midi(line):
    match = re.match(r'(Ctrl \+ |Shift \+ )?([QWERTEYUIO123567])(?: \(([\d.]+) beats?\))?', line.strip())
    if not match:
        return None

    modifier = match.group(1).strip().replace(' +', '') if match.group(1) else ''
    key = match.group(2)
    duration = float(match.group(3)) if match.group(3) else 1.0

    if key not in reverse_key_map:
        return None

    base_note = reverse_key_map[key]
    midi_note = base_note + get_octave_modifier(modifier) * 12

    return midi_note, duration

def validate_file_to_midi(input_path):
    # Extract filename
    base_name = os.path.basename(input_path)
    name_no_ext = os.path.splitext(base_name)[0]
    output_folder = "validation_output"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"validation_{name_no_ext}.mid")

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(60)  # 60 BPM = 1 second per beat
    ticks_per_beat = mid.ticks_per_beat
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    with open(input_path, 'r') as f:
        for line in f:
            result = convert_line_to_midi(line)
            if not result:
                continue
            note, duration = result
            delta_ticks = int(duration * ticks_per_beat)
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=delta_ticks))

    mid.save(output_path)
    print(f"✅ MIDI output written to {output_path}")

if __name__ == "__main__":
    path = input("Path to converted text file (e.g. output/zelda_lullaby.txt): ")
    validate_file_to_midi(path)
