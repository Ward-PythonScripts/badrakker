import pafy
import cv2

badminton_match = "https://www.youtube.com/watch?v=IKDCak_TsHE&ab_channel=BWFTV"
video = pafy.new(badminton_match)
best = video.getbest(preftype="mp4")

capture = cv2.VideoCapture(best.url)
while True:
    grabbed, frame = capture.read()
    cv2.imshow("Frame",frame)
    cv2.waitKey()