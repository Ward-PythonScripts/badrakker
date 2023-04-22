
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2


model = torch.hub.load('ultralytics/yolov5', 'custom', path='workspace/yolov5/runs/train/exp27/weights/last.pt')#, force_reload=True)

cap = cv2.VideoCapture('footage/compilation_1.mp4')

skip_first_frames = 2000 
cap.set(1,skip_first_frames)

while cap.isOpened():
    ret, frame = cap.read()
    # Make detections 
    results = model(frame)
    
    cv2.imshow('YOLO', np.squeeze(results.render()))
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

