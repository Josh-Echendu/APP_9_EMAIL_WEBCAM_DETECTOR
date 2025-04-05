import cv2
import time

video = cv2.VideoCapture(0) #To start a video using a webcam.
time.sleep(1)

while True:

    check, frame = video.read() # after starting the video using a webcam we Read the video, storing it in frame variable
    cv2.imshow("My video", frame) # the frame provides those matrixs of the images
    print(frame)

    key = cv2.waitKey(1) # this create a keyboard key object

    if key == ord('q'): # This means if the user press the 'q' key we shold break the program
        break


video.release()    