import numpy as np
from scipy.signal import welch
import muselsl
from pylsl import StreamInlet, resolve_byprop
import speech_recognition as sr
from gtts import gTTS
import tempfile
import playsound
import google.generativeai as genai
import sys
import torch
import cv2
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import threading

# Configure Gemini API
genai.configure(api_key="AIzaSyCwG_L13ff4nGu1U4ei8Kq9_50EomwQ_Ek")

# Shared state to control YOLOv5 detection
shared_state = {"start_detection": False, "block_person": False}

def llm_parsing(user_text):
    prompt = (
        f"Given what the user said, which is '{user_text}', say what the user is stressed about in one word. "
        "For example, if the user said 'I am getting stressed from people,' the output should just be 'person'. "
        "Nothing else, just one word."
    )
    response = genai.GenerativeModel("gemini-1.5-flash-001").generate_content(prompt)
    return response.text.strip()

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        tts.save(temp_file.name)
        playsound.playsound(temp_file.name)

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
    freqs, psd = welch(eeg_data, fs=sampling_rate, nperseg=1024)
    alpha_band = (8, 12)  # Alpha waves
    beta_band = (12, 30)  # Beta waves
    alpha_power = np.mean(psd[(freqs >= alpha_band[0]) & (freqs <= alpha_band[1])])
    beta_power = np.mean(psd[(freqs >= beta_band[0]) & (freqs <= beta_band[1])])
    return alpha_power, beta_power

def detect_stress(alpha_power, beta_power, threshold=1.0):
    alpha_beta_ratio = alpha_power / beta_power
    return "Stressed" if alpha_beta_ratio <= threshold else "Relaxed"

def real_time_alpha_beta(shared_state):
    print("Looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG')
    inlet = StreamInlet(streams[0])  # Create an inlet to read data

    print("Stream found. Starting real-time processing...")
    chunk_size = 256  # Process data in chunks of 256 samples
    sampling_rate = 256  # Muse S Gen 2 sampling rate
    buffer = np.zeros(chunk_size)
    index = 0

    while True:
        sample, _ = inlet.pull_sample()  # sample contains [channel1, channel2, channel3, channel4]
        eeg_sample = sample[0]  # Use the first channel (FP1) for simplicity
        buffer[index] = eeg_sample
        index += 1

        if index >= chunk_size:
            alpha_power, beta_power = extract_alpha_beta_power(buffer, sampling_rate)
            stress_status = detect_stress(alpha_power, beta_power, threshold=1.0)
            print(f"Alpha Power: {alpha_power:.4f}, Beta Power: {beta_power:.4f}, Status: {stress_status}")

            buffer = np.zeros(chunk_size)
            index = 0

            if stress_status == "Stressed":
                # Ask the user why they are stressed
                speak("It seems that you are stressed. Can you tell me why?")
                user_text = listen_to_user()
                if user_text:
                    stress_item = llm_parsing(user_text)
                    print(f"Detected stress source: {stress_item}")
                    speak(f"It seems you are stressed about {stress_item}.")
                    list1 = []
                    list1.append(stress_item)
                    print(list1)
                    # If the user is stressed from a person, activate YOLOv5 detection and block the person
                    if stress_item.strip() == "person":
                        shared_state["start_detection"] = True
                        print("updated")
                        shared_state["block_person"] = True
                    

def yolo_person_detection(shared_state):
    # Path to the cloned YOLOv5 directory (adjust accordingly)
    sys.path.insert(0, '/yolov5')

    # Load the custom YOLOv5 model
    device = select_device('cuda' if torch.cuda.is_available() else 'cpu')
    model = attempt_load('/Users/savirdillikar/Programming/eeg/yolov5s.pt')  # Provide the correct path to your model

    # Open the camera to capture frames
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Check if frame is valid
        if frame is None:
            print("Error: Frame is None.")
            break

        # Initially, show a blank frame
        if not shared_state["start_detection"]:
            ret, frame = cap.read()
            cv2.imshow("Person Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # Get original frame dimensions
        orig_h, orig_w = frame.shape[:2]

        # Resize the frame to 640x640 (YOLOv5 input size)
        img = cv2.resize(frame, (640, 640))

        # Preprocess the frame for YOLOv5
        img = img.transpose((2, 0, 1))  # Convert frame to channel-first format
        img = np.ascontiguousarray(img)  # Make sure the image is contiguous
        img = torch.from_numpy(img).float()  # Convert to tensor
        img /= 255.0  # Normalize to [0, 1]
        img = img.unsqueeze(0)  # Add batch dimension

        # Run the model on the frame
        with torch.no_grad():
            pred = model(img.to(device))[0]

        # Apply non-max suppression (NMS) to filter out weak detections
        pred = non_max_suppression(pred, conf_thres=0.2, iou_thres=0.50)

        # Check for person detection
        for det in pred:
            if len(det):
                for *xyxy, conf, cls in det:
                    label = model.names[int(cls)]
                    if label == 'person':  # Person detected
                        # Convert xyxy to a tensor
                        xyxy = torch.tensor(xyxy).view(1, 4)  # Convert to tensor and reshape
                        # Scale coordinates back to original frame dimensions
                        xyxy = scale_boxes(img.shape[2:], xyxy, (orig_h, orig_w))  # Use scale_boxes
                        x1, y1, x2, y2 = map(int, xyxy[0])  # Extract coordinates from tensor

                        # Block out the person with a black rectangle
                        if shared_state["block_person"]:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)  # Black rectangle

        # Show the processed frame
        cv2.imshow("Person Detection", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Shared state to control YOLOv5 detection
    shared_state = {"start_detection": False, "block_person": False}

    # Start EEG stress detection in a separate thread
    eeg_thread = threading.Thread(target=real_time_alpha_beta, args=(shared_state,))
    eeg_thread.start()

    # Run YOLOv5 person detection in the main thread
    yolo_person_detection(shared_state)

    # Wait for the EEG thread to finish
    eeg_thread.join()                   