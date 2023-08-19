import RPi.GPIO as GPIO
import time
import requests

TOKEN = "BBFF-V85UAx0mdUZiHeVk66yZoFSF5tS8JC"  # Put your TOKEN here
DEVICE_LABEL = "sensor"  # Put your device label here 
VARIABLE_LABEL_1 = "ultrasonic"  # Put your first variable label here

def build_payload(variable_1, value_1):
    # Creates two random values for sending data

    # Creates a random gps coordinates
    payload = {variable_1: value_1}

    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

GPIO_TRIGGER = 23
GPIO_ECHO = 24

def setup():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
def distance():
    GPIO.output(GPIO_TRIGGER, True)
    
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(GPIO_ECHO)== 0:
        start_time = time.time()
    
    while GPIO.input(GPIO_ECHO)== 1:
        stop_time = time.time()
        
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance
if __name__=='__main__':
    try:
        setup()
        while True:
            dist = distance()
            payload = build_payload(VARIABLE_LABEL_1, dist)

            print("[INFO] Attemping to send data")
            post_request(payload)
            print("[INFO] finished")
            print("Distance: %.2f cm" % dist)
            time.sleep(1)
            
            
    except KeyboardInterrupt:
        GPIO.cleanup()