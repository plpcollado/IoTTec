
import threading
import time
from smbus2 import SMBus
from bme280 import BME280
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import paho.mqtt.client as mqtt

# Temperature Sensor Code
def temperature_sensor():
    try:
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
    except ImportError:
        from smbus import SMBus
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)

    while True:
        temperature = bme280.get_temperature()
        presion = bme280.get_pressure()
        humedad = bme280.get_humidity()
        print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, presion, humedad))
        time.sleep(1)  # Added a sleep to prevent constant resource use

# Rover Control Code
def rover_control():
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
    

   

# Running both functionalities in separate threads
temperature_thread = threading.Thread(target=temperature_sensor)
rover_thread = threading.Thread(target=rover_control)

temperature_thread.start()
rover_thread.start()
