import numpy as np
from scipy.signal import welch
import muselsl
from pylsl import StreamInlet, resolve_byprop
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import tempfile
import playsound
import google.generativeai as genai

def llm_parsing(user_text):
    genai.configure(api_key="AIzaSyCwG_L13ff4nGu1U4ei8Kq9_50EomwQ_Ek")

    prompt = (
      f"given what the user said which is {user_text} say what the user is stressed about in one word"
        "so for example if the user said I am getting stressed from people the output should just be person . Nothing else just person"
        "if I say I get stressed from people you only say person. If I say I get stressed from fire you only say fire"
    )

    # Generate response from Gemini
    response = genai.GenerativeModel("gemini-1.5-flash-001").generate_content(prompt)
    generated_prompt = response.text
    return generated_prompt

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save the speech to a temporary file in memory and play it directly
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        tts.save(temp_file.name)
        playsound.playsound(temp_file.name)



# Set up the text-to-speech engine
engine = pyttsx3.init()

def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except Exception as e:
        print("Sorry, I couldn't understand. Please try again.")
        return None
def extract_alpha_beta_power(eeg_data, sampling_rate=256):
    """
    Extract Alpha and Beta power from EEG data.
    :param eeg_data: Raw EEG data (1D array).
    :param sampling_rate: Sampling rate of the EEG data (default 256 Hz for Muse).
    :return: Alpha power, Beta power.
    """
    # Compute the Power Spectral Density (PSD) using Welch's method
    freqs, psd = welch(eeg_data, fs=sampling_rate, nperseg=1024)

    # Define frequency bands
    alpha_band = (8, 12)  # Alpha waves
    beta_band = (12, 30)  # Beta waves

    # Extract power in the Alpha and Beta bands
    alpha_power = np.mean(psd[(freqs >= alpha_band[0]) & (freqs <= alpha_band[1])])
    beta_power = np.mean(psd[(freqs >= beta_band[0]) & (freqs <= beta_band[1])])

    return alpha_power, beta_power

def detect_stress(alpha_power, beta_power, threshold=1.0):
    """
    Detect stress based on Alpha/Beta ratio.
    :param alpha_power: Alpha power value.
    :param beta_power: Beta power value.
    :param threshold: Threshold for stress detection.
    :return: "Stressed" or "Relaxed".
    """
    alpha_beta_ratio = alpha_power / beta_power
    if alpha_beta_ratio > threshold:
        return "Relaxed"
    else:
        return "Stressed"

def real_time_alpha_beta():
    """
    Stream EEG data from Muse S Gen 2 and extract Alpha/Beta power in real-time.
    """
    # Resolve the EEG stream
    print("Looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG')
    inlet = StreamInlet(streams[0])  # Create an inlet to read data

    print("Stream found. Starting real-time processing...")
    chunk_size = 256  # Process data in chunks of 256 samples
    sampling_rate = 256  # Muse S Gen 2 sampling rate
    buffer = np.zeros(chunk_size)
    index = 0

    while True:
        # Get a new sample from the stream
        sample, _ = inlet.pull_sample()  # sample contains [channel1, channel2, channel3, channel4]
        eeg_sample = sample[0]  # Use the first channel (FP1) for simplicity

        # Add the sample to the buffer
        buffer[index] = eeg_sample
        index += 1

        # Process the chunk when the buffer is full
        if index >= chunk_size:
            # Extract Alpha and Beta power
            alpha_power, beta_power = extract_alpha_beta_power(buffer, sampling_rate)

            # Detect stress
            stress_status = detect_stress(alpha_power, beta_power, threshold=1.0)
            print(f"Alpha Power: {alpha_power:.4f}, Beta Power: {beta_power:.4f}, Status: {stress_status}")

            # Reset the buffer
            buffer = np.zeros(chunk_size)
            index = 0
            if stress_status == "Stressed":
                speak("Why are you stressed")
                user_text = listen_to_user()
                stress_item = llm_parsing(user_text)
                print(stress_item)
                
if __name__ == "__main__":
    real_time_alpha_beta()