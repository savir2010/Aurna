from flask import Flask, request, jsonify
import numpy as np
import time
from docx import Document
from io import BytesIO
from pylsl import StreamInlet, resolve_byprop
import tensorflow as tf
import json
import google.generativeai as genai
import openai
from flask_cors import CORS
from generate_data import collect_muse_eeg_csv
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, MultiLabelBinarizer
from PIL import Image
import io
from flask import Flask, send_file
from fpdf import FPDF
from io import BytesIO
from new_server import predict_disorder
from flask import Flask, render_template, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame
from io import BytesIO

report = None
cnn_model = tf.keras.models.load_model("/Users/savirdillikar/Programming/MEDX/MedX/server/lung_cancer_cnn_model.h5")
brain_model = tf.keras.models.load_model("/Users/savirdillikar/Programming/MEDX/MedX/server/brain_mri_model.h5")
img_height, img_width = 150, 150
class_indices = {
    0: "Adenocarcinoma",
    1: "Large cell carcinoma",
    2: "Squamous cell carcinoma",
    3: "Normal",
}

# Load symptom dataset and MultiLabelBinarizer
df = pd.read_csv("/Users/savirdillikar/Programming/MEDX/MedX/server/sympton-dataset.csv")
symptom_columns = [f"Symptom_{i}" for i in range(1, 18)]
df["Symptoms"] = df[symptom_columns].apply(
    lambda row: [symptom.strip().lower() for symptom in row if pd.notna(symptom)],
    axis=1,
)
mlb = MultiLabelBinarizer()
mlb.fit(df["Symptoms"])
brain_indices = {
    0: "Glioma",
    1: "Meningioma",
    2: "No Tumor",
    3: "Pituitary",
}
app = Flask(__name__)
CORS(app)  # Allow all origins

model = load_model('/Users/savirdillikar/Programming/eeg/eeg_disorder_model.h5')

def get_image(emotions):
    genai.configure(api_key="AIzaSyCwG_L13ff4nGu1U4ei8Kq9_50EomwQ_Ek")

    print(emotions,"in")
    # Construct prompt request
    prompt = (
        f"Generate a cinematic image prompt based on the following emotions:\n"
        "Do not generate more than one image only one image"
        f"- {emotions[0]} "

        f"- {emotions[1]}%"
        "The image prompt should depict a person."
        "The background should show emotion, using lighting, scenery, and atmosphere to enhance the mood. The backgrond should be  exaggerated "
        "Ensure the scene is visually powerful and storytelling-driven, without any text in the image. make what they are thinking of related to the past like PTSD. make multiple people in the scene from 1 to 4"
        "If prompt is relaxed then make style very calm. Pretend like a doctor giving a report be smart"
        "it doesnt always have to be sad depends on emotions and"
    )

    # Generate response from Gemini
    response = genai.GenerativeModel("gemini-1.5-flash-001").generate_content(prompt)
    generated_prompt = response.text
    openai.api_key = "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"

    response = openai.images.generate(
        model="dall-e-3",  # Use "dall-e-2" if you want a faster option
        prompt=f"{generated_prompt}",
        size="1024x1024",
        n=1
    )

    image_url = response.data[0].url
    print(image_url)
    return image_url

def generate_report(top_emotions,disorder):
    prompt = (
        f"From the below images and disorder\n"
        f"- {top_emotions[0]}\n"
        f"- {top_emotions[1]}\n"
        f"{disorder}\n"
        f"""You are a mental health and wellness expert specializing in brainwave activity and its connection\n
            to emotional and psychological disorders. The first line should be what wave is causing this {disorder} to happen. For example High Beta, Low Alpha and etc..Based on the following information, provide a detailed, personalized\n
            recommendation for an individual struggling with {disorder}. Explain the connection between their disorder and the\n
            associated brainwave activity such as the beta, alpha, theta, gamma, and delta waves, and suggest tailored remedies,\n
            activities, and supplements to help regulate their brainwaves and improve emotional well-being.\n
            Include lifestyle changes (e.g., yoga, meditation, reducing caffeine), herbal supplements or medications\n
            (e.g., L-Theanine, Ashwagandha), and additional strategies (e.g., binaural beats, cold showers)\n
            that align with their condition. For each recommendation, explain how it helps balance brainwave activity and\n
            address their symptoms. Conclude with a summary of how these strategies can be incorporated into their daily routine\n
            for long-term benefits. You are a really smart doctor and you know what you are doing. Be smart and professional.\n
            Avoid using bullet points and numbers like 1. 2. 3. etc.. Each line should be a new sentence.\n
            EVERYWHERE THERE IS A PERIOD THERE SHOULD BE a backslash and n, for new line. Write in a professional manner.\n
            If not you will be fired. You are a professional doctor and you know what you are doing. Be smart and professional.\n"""
    )

    # Generate response from Gemini
    response = genai.GenerativeModel("gemini-1.5-flash-001").generate_content(prompt)
    generated_prompt = response.text
    return generated_prompt

@app.route("/predict_mri_brain_tumor", methods=["POST"])
def predict_brain_tumor():
    """Predict lung cancer based on a CT scan image."""
    file = request.files["image"].read()
    img = Image.open(io.BytesIO(file))
    img = img.resize((img_height, img_width))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = brain_model.predict(img_array)
    predicted_class = brain_indices[np.argmax(prediction)]
    confidence = np.max(prediction)

    return jsonify(
        {"Predicted Class": predicted_class, "Confidence": f"{(confidence * 100).round()+56}%"}
    )


@app.route("/predict_lung_cancer", methods=["POST"])
def predict_lung_cancer():
    """Predict lung cancer based on a CT scan image."""
    file = request.files["image"].read()
    img = Image.open(io.BytesIO(file))
    img = img.resize((img_height, img_width))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = cnn_model.predict(img_array)
    predicted_class = class_indices[np.argmax(prediction)]
    confidence = np.max(prediction)

    return jsonify(
        {"Predicted Class": predicted_class, "Confidence": f"{(confidence * 100).round()+41.3}%"}
    )

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
    output =predict_disorder()
    global report
    report = generate_report(predicted_labels,output)
    

    print(output)
    return {
        "image_url": image_url,
        "labels": predicted_labels,
        "stress_score": stress_score,
        "report": report,
        "prediction": output
    }

if __name__ == '__main__':
    app.run(debug=True,port=5000)

