#images are in form of frames which are matrix
import cv2
import backend_email
import glob
import os
from threading import Thread
import time

video = cv2.VideoCapture(0) #To start a video using a webcam.
first_frame = None

status_list = []

# This is connected to the dynamic image
count = 1

def clean_folder():
    print("clean folder has started")
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
    print("clean folder has ended")

while True:
    status = 0 # When the loop starts the status is equal to '0'
    check, frame = video.read() 

    #Convert to gray farm  
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    # The tuple is for the amount of blurness and '0' as for the standard deviation
    # To make the calculation more efficient we use the GaussianBlur method
    gray_fram_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0 )

    if first_frame is None:
        first_frame = gray_fram_gau

    # Difference btw the first_fram and the gray_fram_gau
    # when the loop starts it iterates and initialize the first_frame with gray_frame_gau, when it iterates again it compares the
    # Difference btw the first_fram and gray_frame_gau which means when if there is no object in the first frame, and then, there is an object in the
    #gray_fram_gau, the delta_frame variable checks the difference between the frame where there is no object with a frame where there is an object

    delta_frame = cv2.absdiff(first_frame, gray_fram_gau) 
    cv2.imshow("My video", delta_frame)
    #print(delta_frame)# you would observe when there is no object the we have 0, 1, 2 pixels as values(black pixels) in the matrix den when an object comes in we see 50, 7o, 100 pixels as values (white pixels)

    # Classify the pixels based on a threshold, by only black and white in the frame, which means we would have only white pixel
    # when there is an object in the frame, and black pixels when there is no object
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    
    # To remove the noise i.e the sparking on the object in the frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)  # the higher you go with the iteration the more processing you get
    cv2.imshow("My video", dil_frame)
    
    # To Find contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # They are used to detect contours around those white areas

    # IF there is more than one object and we want to draw countours for all the objects And calculate the areas around all the objects
    # That is if the area is smaller than an '10000', '5000' or etc, then it is fake positive which is, it is not a real object
    # Coutours variable contains a list of contour objects as value, and if there are two object there would be two contour    
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        # we are extracting the corners, width and height of the object
        x, y, w, h = cv2.boundingRect(contour)

        # We draw a rectangle around the frame with a green((0, 255, 0)) color
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) 
        
        # if it notices an object through the rectangle it calls the function 
        if rectangle.any():
            status = 1 # if it notice an object the status variable is updated to '1'
        
            # To create an image
            cv2.imwrite(f'images/{count}.png', frame)
            count = count + 1
            
            # Create list of images
            all_images = glob.glob('images/*.png')
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    status_list.append(status)  

    # We get the last two values of status_list
    status_list = status_list[-2:]
    
    #if the condition below is True it means the object just exited the frame
    if status_list[0] == 1 and status_list[1] == 0:

        # Call the function to send file path Using Threading
        email_thread = Thread(target=backend_email.send_email, args=(image_with_object,))  # Notice the comma after image_with_object
        email_thread.daemon = True
        

        email_thread.start()

    print(status_list)
    cv2.imshow("video", frame)
    key = cv2.waitKey(1) # this create a keyboard key object

    if key == ord('q'): # This means if the user press the 'q' key we shold break the program 
        break


video.release()

clean_thread = Thread(target=clean_folder)  # Start clean thread outside the loop
clean_thread.daemon = True
clean_thread.start()
time.sleep(0.1)