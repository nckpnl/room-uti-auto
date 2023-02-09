import RPi.GPIO as GPIO
import time
import datetime
import cv2

GPIO.setmode(GPIO.BCM)

pinList = [2, 3, 4, 17]

GPIO.setup(2, GPIO.OUT)#power_outlets
GPIO.setup(3, GPIO.OUT)#lights
GPIO.setup(4, GPIO.OUT)#fan
GPIO.setup(17, GPIO.OUT)#blank
x = 1
SleepTimeL = 2

# Initialization sequence
GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
GPIO.output(4, GPIO.HIGH)
GPIO.output(17, GPIO.HIGH)
time.sleep(SleepTimeL)
GPIO.output(17, GPIO.LOW)
print("initializing...")
print("one-blank")
time.sleep(SleepTimeL)
GPIO.output(4, GPIO.LOW)
print("two-fans")
time.sleep(SleepTimeL)
GPIO.output(3, GPIO.LOW)
print("three-lights")
time.sleep(SleepTimeL)
GPIO.output(2, GPIO.LOW)
print("four-power outlets")
time.sleep(SleepTimeL)
GPIO.output(17, GPIO.HIGH)
GPIO.output(4, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
GPIO.output(2, GPIO.HIGH)
time.sleep(SleepTimeL)
GPIO.output(17, GPIO.LOW)
GPIO.output(4, GPIO.LOW)
GPIO.output(3, GPIO.LOW)
GPIO.output(2, GPIO.LOW)
time.sleep(SleepTimeL)
GPIO.output(17, GPIO.HIGH)
GPIO.output(4, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
GPIO.output(2, GPIO.HIGH)
print("done!!")


# Set the camera index to 0 (usually the built-in webcam on a laptop)
# Set to 1 or higher if you have multiple cameras connected
camera_index = 0

# Start the camera capture
cap = cv2.VideoCapture(camera_index)

# Set the frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Load the Haar cascade classifiers for detecting people and faces
people_cascade = cv2.CascadeClassifier('/home/admin/Desktop/autorun_final/haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier('/home/admin/Desktop/autorun_final/haarcascade_frontalface_default.xml')
upperbody_cascade = cv2.CascadeClassifier('/home/admin/Desktop/autorun_final/haarcascade_upperbody.xml')

# Set the delay time in seconds
delay_time = 60


# Main loop
while True:
    
    # Capture a frame from the camera
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect people and faces in the frame
    people = people_cascade.detectMultiScale(gray, 1.3, 5)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    upbody = upperbody_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Draw boxes around detected people and faces
    for (x, y, w, h) in people:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    for (x, y, w, h) in upbody:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Display the frame
    cv2.imshow('Video', frame)


    # Check if any people or faces were detected
    if len(people) > 0 or len(faces) > 0 or len(upbody):
        GPIO.output(3, GPIO.LOW)#on lights
        print("light on")
        
        if len(people) > 1 or len(faces) > 1 or len(upbody) > 1:
            GPIO.output(4, GPIO.LOW)#on fan
            print("fan on")
            
        elif len(people) == 0 or len(faces) == 0 or len(upbody) == 0:
            # Sleep for the specified delay time
            time.sleep(delay_time)
            GPIO.output(4, GPIO.HIGH)#off fan
            print("fan off")
        else:
            print("fan off")
            
    elif len(people) == 0 or len(faces) == 0 or len(upbody) == 0:
        if GPIO.input(3) == GPIO.LOW:
            # Sleep for the specified delay time
            time.sleep(delay_time)
            # Set the output pin to high
            GPIO.output(3, GPIO.HIGH)
        else:
            print("state continue")

    # Check the current time
    now = datetime.datetime.now()

     # Set the output pin to high from 7:00 AM to 7:00 PM
    if now.hour >= 7 and now.hour < 19:
        GPIO.output(2, GPIO.LOW)
    else:
        # Set the output pin to low outside of these hours
        GPIO.output(2, GPIO.HIGH)
    
    # Check for the 'q' key being pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy the windows
cap.release()
cv2.destroyAllWindows()

# Reset the GPIO settings
GPIO.cleanup()
