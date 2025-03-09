import pygame
import numpy as np
import cv2
import mediapipe as mp
from pylsl import StreamInlet, resolve_byprop
import math
import random

# 🎯 Initialize EEG stream from Muse S
streams = resolve_byprop('type', 'EEG', timeout=5)
if streams:
    inlet = StreamInlet(streams[0])
else:
    raise RuntimeError("No EEG stream found. Please ensure the Muse headset is connected.")

# 🎯 Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

# 🎯 Initialize Pygame for real-time drawing
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Brainwave-Powered Art")
clock = pygame.time.Clock()

# 🎨 Brush settings (default)
brush_size = 2  # Smaller brush size
drawing = False  # Track whether the user is drawing

# 🎨 Button settings
button_color = (255, 0, 0)  # Red button
button_rect = pygame.Rect(650, 550, 120, 40)  # Button position & size

# 🧠 Function to map EEG values to brush color & size
def process_eeg_data():
    try:
        sample, _ = inlet.pull_sample()
        eeg_values = np.array(sample[:4])  # Use first 4 channels
        
        # Normalize EEG values to [0, 1]
        normalized_values = (eeg_values - np.min(eeg_values)) / (np.max(eeg_values) - np.min(eeg_values) + 1e-6)
        
        # Increase frequency drastically for fast color fluctuations
        frequency_factor = random.randint(50, 150)  # Randomized for more variation
        
        red = int(127 * (math.sin(normalized_values[0] * 2 * math.pi * frequency_factor) + 128))
        green = int(127 * (math.sin(normalized_values[1] * 2 * math.pi * frequency_factor + math.pi / 3) + 128))
        blue = int(127 * (math.sin(normalized_values[2] * 2 * math.pi * frequency_factor + math.pi * 2 / 3) + 128))
        
        # Add random fluctuations based on EEG input
        red = np.clip((red * 15 + random.randint(-50, 50)) % 255, 0, 255)
        green = np.clip((green * 15 + random.randint(-50, 50)) % 255, 0, 255)
        blue = np.clip((blue * 15 + random.randint(-50, 50)) % 255, 0, 255)
        
        # Slightly fluctuate brush size based on EEG data
        size = max(1, int(np.mean(normalized_values) * 10 + random.randint(0, 3)))
        
        return (int(red), int(green), int(blue)), size
    except Exception as e:
        print(f"Error in processing EEG data: {e}")
        return (0, 0, 0), 1  # Default if EEG fails

# 🎨 Main loop
running = True
start_drawing_message = True  # Variable to track if we are showing the start drawing message

while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # 🧠 Get EEG-based brush color & size
    brush_color, brush_size = process_eeg_data()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 🎯 Detect button click to clear the screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                screen.fill((0, 0, 0))  # Clear screen

            # Start drawing when user clicks on the screen
            if start_drawing_message:  # Only activate drawing after the message
                start_drawing_message = False  # Disable message once clicked

    # ✍️ Draw based on hand tracking (only if drawing is enabled)
    if not start_drawing_message:  # Only allow drawing once the user clicks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_x = screen.get_width() - int(hand_landmarks.landmark[8].x * screen.get_width())
                index_y = int(hand_landmarks.landmark[8].y * screen.get_height())

                # ✋ Check if index finger is extended before drawing
                index_tip = hand_landmarks.landmark[8].y
                index_base = hand_landmarks.landmark[6].y
                drawing = index_tip < index_base  # Finger extended → Draw

                if drawing:
                    pygame.draw.circle(screen, brush_color, (index_x, index_y), brush_size)

    # 🎨 Draw the "Clear Board" button
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.Font(None, 24)
    text_surface = font.render("Clear Board", True, (255, 255, 255))
    screen.blit(text_surface, (button_rect.x + 15, button_rect.y + 10))

    # 🖊️ Display start drawing message if the user hasn't clicked yet
    if start_drawing_message:
        font = pygame.font.Font(None, 48)
        message = font.render("Click to Start Drawing!", True, (255, 255, 255))
        screen.blit(message, (250, 250))  # Position the message at the center

    pygame.display.flip()
    clock.tick(60)

cap.release()
pygame.quit()
