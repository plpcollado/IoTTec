import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import threading
import paho.mqtt.client as mqtt

# MQTT Setup
mqtt_broker = "192.168.1.128"
mqtt_port = 1883
mqtt_topic_sensor = "rover/sensor"
mqtt_topic_command = "rover/command"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic_command)

def on_message(client, userdata, message):
    command = str(message.payload.decode("utf-8"))
    print(f"Received command: {command}")
    if command == "forward":
        start_forward()
    elif command == "reverse":
        start_reverse()
    elif command == "stop":
        stop()

# Motor Control Functions (as previously defined)
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

def start_forward():
    init()
    GPIO.output(17, True)
    GPIO.output(22, False)
    GPIO.output(23, False) 
    GPIO.output(24, True)

def start_reverse():
    init()
    GPIO.output(17, False)
    GPIO.output(22, True)
    GPIO.output(23, True) 
    GPIO.output(24, False)

def stop():
    GPIO.output(17, False)
    GPIO.output(22, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.cleanup()

# Sensor Reading Function
def read_distance(client):
    sensor = DistanceSensor(echo=9, trigger=10)
    while True:
        distance = sensor.distance * 100
        client.publish(mqtt_topic_sensor, distance)
        time.sleep(0.5)

# Main Function
def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()

    distance_thread = threading.Thread(target=read_distance)
    distance_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped")
        client.loop_stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()