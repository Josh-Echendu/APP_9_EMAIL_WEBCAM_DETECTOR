import glob
import cv2
import time
import backend_email
import os
from threading import Thread

# Initialize video capture and allow camera to warm up
video = cv2.VideoCapture(0)
#time.sleep(2)  # Increased sleep time to ensure camera initialization

# Initialize variables
first_frame = None
status_list = [0, 0]  # Initialize with two elements to avoid initial IndexError
count = 1

def clean_folder():
    """Deletes all PNG images in the 'images' directory."""
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)

while True:
    status = 0  # Initial status: no object detected

    # Capture frame and convert to grayscale
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur for noise reduction (adjusted for efficiency)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Initialize first frame if needed
    if first_frame is None:
        first_frame = gray_frame_gau

    # Calculate frame difference to detect motion
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Display delta frame for debugging (optional)
    # cv2.imshow("Delta Frame", delta_frame)  # Uncomment if needed

    # Threshold the difference frame for binary classification
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # Remove noise (adjust iterations as needed)
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contours around potential objects
    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Handle potential empty contours gracefully
    if not contours:
        continue  # Skip to the next frame if no contours are found

    # Process each contour (consider object filtering based on area if needed)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if rectangle.any():
            status = 1  # Update status if an object is detected

            # Capture image with object for potential email sending
            cv2.imwrite(f'images/{count}.png', frame)
            count += 1

    # Update status list and check for object exiting the frame
    status_list.append(status)
    status_list = status_list[-2:]  # Maintain a list of the last two elements

    # Check if there are at least two elements in the list before accessing them
    if len(status_list) >= 2 and status_list[0] == 1 and status_list[1] == 0:
        # Object detected and then exited the frame: send email and clean folder

        # Choose the latest image (consider filtering for better selection)
        all_images = glob.glob('images/*.png')
        if all_images:
            image_with_object = all_images[-1]  # Use the latest image

            # Send email with image in a separate thread
            email_thread = Thread(target=backend_email.send_email, args=(image_with_object,))
            email_thread.daemon = True
            

            # Clean the images folder in a separate thread
            clean_thread = Thread(target=clean_folder)
            clean_thread.daemon = True
            

            email_thread.start()

    # Display status list and video frame
    print(status_list)
    cv2.imshow("Video", frame)

    print(status_list)
    cv2.imshow("video", frame)
    key = cv2.waitKey(1) # this create a keyboard key object

    if key == ord('q'): # This means if the user press the 'q' key we shold break the program 
        break


video.release()

#This would start the thread and the thread would start the email function
clean_thread.start()