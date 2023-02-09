import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)

pinList = [2, 3, 4, 17]

GPIO.setup(2, GPIO.OUT)#power_outlets
GPIO.setup(3, GPIO.OUT)#lights
GPIO.setup(4, GPIO.OUT)#fan
GPIO.setup(17, GPIO.OUT)#blank
x = 1
SleepTimeL = 2




# Main loop
while True:
    
    people = 1



    # Check if any people or faces were detected
    if people > 0:
        
        GPIO.output(3, GPIO.LOW) #on lights
        print("light on")
        
        if people > 1 :
            GPIO.output(4, GPIO.LOW) #on fan
            print("fan on")
            
        elif people == 0:
            GPIO.output(4, GPIO.HIGH)
            print("fan off")
        else:
            print("fan off")
    elif people == 0:
        
        
        if GPIO.input(3) == GPIO.LOW:
            GPIO.output(3, GPIO.HIGH)
        else:
            print("state continue")

    # Check the current time
    now = datetime.datetime.now()

     # Set the output pin to high from 7:00 AM to 7:00 PM
    if now.hour >= 7 and now.hour < 19:
        GPIO.output(2, GPIO.LOW)#on power outlets
    else:
        # Set the output pin to low outside of these hours
        GPIO.output(2, GPIO.HIGH)#off power outlets
    

    


# Reset the GPIO settings
GPIO.cleanup()
