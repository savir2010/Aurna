import numpy as np
import time
from pylsl import StreamInlet, resolve_byprop
#  Doctor Helps Patient - Thoughts of care, empathy, concern;
#  Sister argues with brother - Thoughts of conflict, frustration;
#  Fire burns house - Thoughts of emergency, fear, rapid reaction;
#  Child cries for mother - Thoughts of sadness and distress;
#  Null - To account for no thoughts
# Connect to Muse EEG stream
print("Searching for Muse EEG stream...")
streams = resolve_byprop('type', 'EEG')

if not streams:
    raise RuntimeError("No EEG stream found. Make sure the Muse device is connected and streaming.")

inlet = StreamInlet(streams[0])
print("Connected to Muse EEG stream!")

# Parameters
num_samples = 50  # 50 recordings
recording_time = 10  # Each recording lasts 10 seconds
fs = 256  # Muse sampling rate (samples per second)
total_samples = recording_time * fs  # Total EEG points per recording

eeg_data = []
labels = []

THOUGHT_LABELS = ["dhp", "sab", "fbh", "cfm", "null"]  # Thought categories

for i in range(num_samples):
    print(f"Recording Sample {i+1}/{num_samples} - Think about: {THOUGHT_LABELS[i % 5]}")
    sample_buffer = []
    start_time = time.time()

    while time.time() - start_time < recording_time:
        sample, _ = inlet.pull_sample()
        if sample:
            sample_buffer.append(sample[:4])  # Use TP9, AF7, AF8, TP10

    eeg_data.append(np.array(sample_buffer))
    labels.append(i % 5)  # Assign thought category

    print("Recording complete.\n")

# Convert to NumPy arrays for processing
eeg_data = np.array(eeg_data, dtype=object)
labels = np.array(labels)

# Save data
np.save("muse_eeg_data.npy", eeg_data)
np.save("muse_eeg_labels.npy", labels)
print("EEG data saved successfully!")
