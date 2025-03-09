import numpy as np
import time
from pylsl import StreamInlet, resolve_byprop

# Connect to Muse EEG stream
print("Searching for Muse EEG stream...")
streams = resolve_byprop('type', 'EEG')

if not streams:
    raise RuntimeError("No EEG stream found. Make sure  he Muse device is connected and streaming.")

inlet = StreamInlet(streams[0])
print("Connected to Muse EEG stream!")  

# Parameters
recording_time = 10  # 10 seconds
fs = 256  # Muse sampling rate (samples per second)
total_samples = recording_time * fs  # Total EEG points per recording

THOUGHT_LABELS = ["dhp", "sab", "fbh", "cfm", "null"]
thought_label = THOUGHT_LABELS[0]  # Modify this if you want a different label

print(f"Recording - Think")

# Record EEG data
sample_buffer = []
start_time = time.time()

while time.time() - start_time < recording_time:
    sample, _ = inlet.pull_sample()
    if sample:
        sample_buffer.append(sample[:4])  # Use TP9, AF7, AF8, TP10

# Convert to NumPy array
eeg_data = np.array(sample_buffer)

# Save as a raw NumPy array in a text file
filename = "eeg_recording.txt"
np.savetxt(filename, eeg_data, fmt="%.6f")

print(f"Recording complete. Data saved to {filename}")
