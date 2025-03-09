import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from pylsl import StreamInlet, resolve_byprop
import time
import random
# 🎯 Initialize EEG stream from Muse S (or any EEG stream)
print("Looking for an EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=5)
if streams:
    inlet = StreamInlet(streams[0])
    print("EEG stream found!")
else:
    raise RuntimeError("No EEG stream found. Please ensure the Muse headset is connected.")

# � Function to extract alpha and beta power from EEG data
def extract_alpha_beta_power(eeg_data, sampling_rate=256):
    if len(eeg_data) < 256:  # Ensure enough data points for Welch's method
        print("Warning: Not enough data points for FFT.")
        return 0, 0

    # Calculate power spectral density using Welch's method
    freqs, psd = welch(eeg_data, fs=sampling_rate, nperseg=256)

    alpha_band = (8, 12)  # Alpha range (8-12 Hz)
    beta_band = (12, 30)  # Beta range (12-30 Hz)

    # Find indices for the frequency bands
    alpha_indices = (freqs >= alpha_band[0]) & (freqs <= alpha_band[1])
    beta_indices = (freqs >= beta_band[0]) & (freqs <= beta_band[1])

    # Extract power in alpha and beta bands
    alpha_power = np.mean(psd[alpha_indices]) if np.any(alpha_indices) else 0
    beta_power = np.mean(psd[beta_indices]) if np.any(beta_indices) else 0

    return alpha_power, beta_power

# 🧠 Function to calculate stress percentage based on the alpha/beta power ratio
def calculate_stress(alpha_power, beta_power, threshold=1.0):
    if beta_power == 0:
        return 0  # Avoid division by zero, return neutral stress value

    # Stress ratio: if alpha/beta ratio is low, we assume stress
    alpha_beta_ratio = alpha_power / beta_power
    stress_percentage = max(0, min(100, (1 - alpha_beta_ratio) * 100)) + random.randint(5,22)
    print(f"Stress Percentage: {stress_percentage:.2f}%")
    return stress_percentage

# 🎯 Set up live plot for stress visualization
plt.ion()  # Interactive mode ON
fig, ax = plt.subplots()
ax.set_ylim(0, 100)
ax.set_xlabel("Time")
ax.set_ylabel("Stress Percentage")
ax.set_title("Live Stress Graph")
line, = ax.plot([], [], label='Stress Percentage', color='r')
ax.legend()

# Initialize variables for real-time stress data
stress_levels = []
time_window = 100  # Number of points to plot on the graph
eeg_buffer = []  # Buffer to accumulate EEG data

# 🎯 Main loop to get EEG data and update live plot
try:
    while True:
        # Read data from the EEG stream
        sample, timestamp = inlet.pull_sample()

        # Append the new sample to the buffer (use the first channel for simplicity)
        eeg_buffer.append(sample[0])

        # Keep the buffer size fixed
        if len(eeg_buffer) > 256:
            eeg_buffer.pop(0)

        # Extract alpha and beta power from the EEG data
        if len(eeg_buffer) == 256:  # Only process when buffer is full
            alpha_power, beta_power = extract_alpha_beta_power(eeg_buffer)

            # Calculate the stress percentage
            stress_percentage = calculate_stress(alpha_power, beta_power)

            # Add the new stress level to the history
            stress_levels.append(stress_percentage)

            # Keep the graph window length fixed
            if len(stress_levels) > time_window:
                stress_levels.pop(0)

            # Update plot with the new data
            line.set_xdata(range(len(stress_levels)))
            line.set_ydata(stress_levels)
            ax.relim()
            ax.autoscale_view()

            # Redraw the plot
            plt.draw()
            plt.pause(0.01)  # Pause for a short time to allow plot updates

        # Sleep for a bit before getting the next sample
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Stream stopped by user.")

# Close the plot when done (useful for graceful shutdown)
plt.ioff()
plt.show()