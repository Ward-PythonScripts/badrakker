import cv2

FOOTAGE_PATH = "footage/swiss_md.mp4"
from tkinter import filedialog


capture = cv2.VideoCapture(FOOTAGE_PATH)
while True:
    grabbed, frame = capture.read()
    cv2.imshow("Frame",frame)
    cv2.waitKey(1000)