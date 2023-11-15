import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import threading
import paho.mqtt.client as mqtt

mqtt_broker = "192.168.1.128"
mqtt_port = 1883
mqtt_topic = "rover/distance"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client.on_connect = on_connect

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
    GPIO.cleanup()

def read_distance():
    sensor = DistanceSensor(echo=9, trigger=10)
    while True:
        cm = sensor.distance * 100
        client.publish(mqtt_topic, cm)

        if cm > 15:
            start_forward()
        else:
            start_reverse()

        time.sleep(0.1)  # Adjust for responsiveness


def main():
    distance_thread = threading.Thread(target=read_distance)
    distance_thread.start()

    # You can add more threads if needed for other tasks

if __name__ == '__main__':
    main()  