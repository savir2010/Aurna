import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop
from scipy.signal import butter, lfilter
import mne

# Define EEG frequency bands
BANDS = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 12),
    "Beta": (12, 30),
    "Gamma": (30, 100)
}

# Bandpass filter function
def bandpass_filter(data, lowcut, highcut, fs=256, order=4):
    nyquist = 0.5 * fs  # Nyquist frequency
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    return lfilter(b, a, data)

# Resolve EEG stream
print("Looking for an EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=5)

if not streams:
    raise RuntimeError("No EEG stream found. Make sure Muse S is streaming.")

inlet = StreamInlet(streams[0])
fs = 256  # Muse S sampling rate

# Initialize buffer
buffer_size = 256  # 1 second of data
eeg_buffer = np.zeros((buffer_size,))
time_series = np.arange(buffer_size) / fs

# Setup plot
plt.ion()
fig, ax = plt.subplots(len(BANDS), 1, figsize=(10, 8))
lines = {}
for i, (band, (low, high)) in enumerate(BANDS.items()):
    lines[band], = ax[i].plot(time_series, np.zeros_like(time_series))
    ax[i].set_title(f"{band} Wave ({low}-{high} Hz)")
    ax[i].set_ylim(-50, 50)
    ax[i].set_xlim(0, buffer_size/fs)

print("Receiving EEG data...")

while True:
    sample, _ = inlet.pull_sample()
    
    # Update buffer
    eeg_buffer = np.roll(eeg_buffer, -1)
    eeg_buffer[-1] = sample[0]  # Use first EEG channel

    # Filter and update plots
    for band, (low, high) in BANDS.items():
        filtered_signal = bandpass_filter(eeg_buffer, low, high, fs)
        lines[band].set_ydata(filtered_signal)

    plt.draw()
    plt.pause(0.01)
