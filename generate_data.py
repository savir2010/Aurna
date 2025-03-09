import numpy as np
import pandas as pd
from scipy.signal import welch
from muselsl import list_muses
from pylsl import StreamInlet, resolve_byprop
import time

def collect_muse_eeg_csv(filename="muse_eeg.csv", duration=10, fs=256):
    """Collect real-time EEG data from Muse using LSL and extract features."""
    print("Looking for a Muse EEG stream...")
    streams = resolve_byprop('type', 'EEG', timeout=10)
    
    if not streams:
        print("No Muse EEG stream found. Make sure Muse is connected and streaming.")
        return
    
    inlet = StreamInlet(streams[0])
    print("Connected to Muse stream. Collecting data...")
    
    channels = ["AF7", "AF8", "TP9", "TP10"]
    channel_map = {"TP9": "T3", "TP10": "T4", "AF7": "F7", "AF8": "F8"}
    freq_bands = {
        "delta": (0.5, 4), "theta": (4, 8), "alpha": (8, 12),
        "beta": (12, 30), "highbeta": (20, 30), "gamma": (30, 50)
    }
    
    eeg_data = {ch: [] for ch in channels}
    start_time = time.time()
    
    while time.time() - start_time < duration:
        sample, _ = inlet.pull_sample()
        for i, ch in enumerate(channels):
            eeg_data[ch].append(sample[i])
    
    print("Data collection complete. Processing...")
    
    data = {"age": 18}  # Random age placeholder
    
    # Compute absolute band power for each channel
    for band, (low_f, high_f) in freq_bands.items():
        for muse_ch, dataset_ch in channel_map.items():
            f, Pxx = welch(eeg_data[muse_ch], fs=fs, nperseg=fs)
            band_power = np.mean(Pxx[(f >= low_f) & (f <= high_f)])
            data[f"AB.{band}.{dataset_ch}"] = band_power

    # Compute coherence (Placeholder values)
    for band in freq_bands.keys():
        data[f"COH.{band}.T3.T4"] = np.random.uniform(0, 1)
        data[f"COH.{band}.F7.F8"] = np.random.uniform(0, 1)
    
    df = pd.DataFrame([data])
    df.to_csv(filename, index=False)
    print(f"Processed EEG data saved to {filename}")

# Run the function
# collect_muse_eeg_csv(duration=10)
