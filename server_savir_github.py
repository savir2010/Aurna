from flask import Flask, request, jsonify
import numpy as np
import time
from pylsl import StreamInlet, resolve_byprop
import tensorflow as tf
import json
import google.generativeai as genai
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

def get_image(emotions):
    genai.configure(api_key="gemini key")

    print(emotions,"in")
    # Construct prompt request
    prompt = (
        f"Generate a cinematic image prompt based on the following emotions:\n"
        "Do not generate more than one image only one image"
        f"- {emotions[0]} "

        f"- {emotions[1]}%"
        "The image prompt should depict a person."
        "The background should convey more emotion than the person, using lighting, scenery, and atmosphere to enhance the mood. The backgrond should be slightly exaggerated "
        "Ensure the scene is visually powerful and storytelling-driven, without any text in the image. make what they are thinking of related to the past like PTSD. make multiple people in the scene from 1 to 4"
        "If prompt is relaxed then make style very calm. Pretend like a doctor giving a report be smart"
        "it doesnt always have to be sad depends on emotions and confidence. Depending on the confindence stress on that emotion"
    )

    # Generate response from Gemini
    response = genai.GenerativeModel("gemini-1.5-pro-001").generate_content(prompt)
    generated_prompt = response.text
    openai.api_key = "OPENAI KEY"

    response = openai.images.generate(
        model="dall-e-3",  # Use "dall-e-2" if you want a faster option
        prompt=f"{generated_prompt}",
        size="1024x1024",
        n=1
    )

    image_url = response.data[0].url
    print(image_url)
    return image_url

def generate_report(top_emotions):
    prompt = (
    f"Generate a cinematic image prompt based on the following emotions:\n"
    f"- {top_emotions[0]}"
    f"- {top_emotions[1]}"
    "from the two emotions generate a report to give to the doctor stating what the user may be going through. This is not an image prompt this is a proffessional doctor prompt. It does not matter how accurate, just an educated guess."

)

    # Generate response from Gemini
    response = genai.GenerativeModel("gemini-1.5-pro-001").generate_content(prompt)
    generated_prompt = response.text
    return generated_prompt

@app.route('/record_predict', methods=['POST','GET'])
def record_api():
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
    # total_samples = recording_time * fs  # Total EEG points per recording

    THOUGHT_LABELS = ["dhp", "sab", "fbh", "cfm", "null"]

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
    filename = "eeg_recording.txt"
    eeg_file = np.loadtxt(filename, dtype=np.float32)

    # Define target shape
    # target_samples = 2556
    # num_channels = 4

    # Ensure it's a NumPy array
    eeg_file = np.array(eeg_file, dtype=np.float32)
    eeg_file = eeg_file[:2556, :]
    eeg_file = eeg_file.reshape(1, 2556, 4)
    model = tf.keras.models.load_model("brain_eeg_predict.h5")
    predictions = model.predict(eeg_file)
    print(predictions[0])
    # Get the predicted class
    predicted_class = np.argmax(predictions, axis=1)[0]  # Returns the class index
    print(predicted_class)
    # Define class labels
    top_2_indices = np.argsort(predictions[0])[-2:][::-1]

    print(top_2_indices)

    class_labels = ['relaxed', 'frustration', 'emergency trauma', 'sadness', 'null']
    predicted_labels = list([class_labels[i] for i in top_2_indices])

    # Convert to JSON
    json_output = json.dumps(predicted_labels, indent=2)
    image_url = get_image(json_output)
    stress_score = float(predictions[0][top_2_indices[0]] + predictions[0][top_2_indices[1]])
    image_url = get_image(json_output)
    report = generate_report(predicted_labels)

    return {
        "image_url": image_url,
        "labels": predicted_labels,
        "stress_score": stress_score,
        "report": report
    }

if __name__ == '__main__':
    app.run(debug=True,port=1222)

