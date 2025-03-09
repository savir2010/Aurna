import sys
import torch
import cv2
import numpy as np
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

# Path to the cloned YOLOv5 directory (adjust accordingly)
sys.path.insert(0, '/yolov5')

# Load the custom YOLOv5 model
device = select_device('cuda' if torch.cuda.is_available() else 'cpu')
model = attempt_load('/Users/savirdillikar/Programming/eeg/yolov5s.pt')  # Provide the correct path to your model

# Open the camera to capture frames
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

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
                    # Draw a rectangle around the person
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle

    # Show the processed frame
    cv2.imshow("Person Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()