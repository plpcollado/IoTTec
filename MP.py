import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import threading
import mysql.connector
from smbus2 import SMBus
from bme280 import BME280

# Database Configuration
db_host = "retocarritocloud.czosggbj7hr7.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "8ik9FiE2AgE*"  # Replace with your actual password
db_name = "micarrito"

# Global variables for sensor data
current_distance = None
current_temperature = None

# Function to insert both temperature and distance into the database
def insertar_datos(temperatura, distancia):
    try:
        conexion = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conexion.cursor()
        query = "INSERT INTO carrito (temperatura, distancia) VALUES (%s, %s);"
        cursor.execute(query, (temperatura, distancia))
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error al insertar en la base de datos:", e)

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
    global current_distance
    sensor = DistanceSensor(echo=9, trigger=10)
    while True:
        current_distance = sensor.distance * 100
        # Control movement based on distance
        if current_distance > 15:
            start_forward()
        else:
            start_reverse()
        time.sleep(0.1)

# Sensor Configuration
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

def read_temperature():
    global current_temperature
    while True:
        current_temperature = bme280.get_temperature()
        time.sleep(0.1)  # Adjust as needed

def data_insertion_loop():
    global current_temperature, current_distance
    while True:
        if current_temperature is not None and current_distance is not None:
            insertar_datos(current_temperature, current_distance)
        time.sleep(5)  # Insert data every 5 seconds

def main():
    distance_thread = threading.Thread(target=read_distance)
    temperature_thread = threading.Thread(target=read_temperature)
    insertion_thread = threading.Thread(target=data_insertion_loop)

    distance_thread.start()
    temperature_thread.start()
    insertion_thread.start()

if __name__ == '__main__':
    main()
