#images are in form of frames which are matrix
import cv2
import time

video = cv2.VideoCapture(0) #To start a video using a webcam.
time.sleep(1)
first_frame = None

while True:

    check, frame = video.read() 

    # convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # The tuple is for the amount of blurness and '0' as for the standard deviation
    # To make the calculation more efficient we use the GaussianBlur method
    gray_fram_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0 )
    

    if first_frame is None:
        first_frame = gray_fram_gau

    # Difference btw the first_fram and the gray_fram_gau
    delta_frame = cv2.absdiff(first_frame, gray_fram_gau)
    cv2.imshow("My video", delta_frame)

    # Classify the pixels based on a threshold, by only black and white in the frame, which means we would hve only white pixel when there is an object,
    # and black pixels when there is no object
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    
    # To remove the noise i.e the sparking on the object in the frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)  # the higher you go with the iteration the more processing you get
    cv2.imshow("My video", dil_frame)
    
    # To Find contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # They are used to detect contours around those white areas

    # IF WE OBSERVE more than one object and we want to draw countours for all the objects And calculate the areas around all the objects
    # That is if the area is smaller than an '10000', then it is fake positive which is, it is not a real object
    # Coutours varriable contains a list of contour objects as value, and if there are two object there would be two contour    
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        # we are extracting the corners, width and height of the object
        x, y, w, h = cv2.boundingRect(contour)

        # This draw a rectangle around the frame with a green((0, 255, 0)) color
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) 
    
    cv2.imshow("video", frame)
    key = cv2.waitKey(1) # this create a keyboard key object

    if key == ord('q'): # This means if the user press the 'q' key we shold break the program 
        break


video.release()    