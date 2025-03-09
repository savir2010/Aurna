import numpy as np

# Load the data
eeg_data = np.load("muse_eeg_data.npy", allow_pickle=True)
labels = np.load("muse_eeg_labels.npy")

# Print shape of the loaded data
print("EEG Data Shape:", eeg_data.shape)  # (num_samples, time_steps, 4)
print("Labels Shape:", labels.shape)  # (num_samples,)

# Print first EEG sample (raw data from 4 channels)
print("First EEG Sample:\n", eeg_data[0])

# Print first label
print("First Label:", labels[0])
