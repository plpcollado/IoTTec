import time
import mysql.connector
from smbus2 import SMBus
from bme280 import BME280

import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import threading

# Configuración de la conexión a la base de datos MySQL
db_host = "retocarritocloud.czosggbj7hr7.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "8ik9FiE2AgE*"
db_name = "micarrito"


#Temperatura------------------------------------

# Configuración del sensor de temperatura
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Función para insertar la temperatura en la base de datos
# def insertar_temperatura(temperatura):
#     try:
#         conexion = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
#         cursor = conexion.cursor()
#         query = "INSERT INTO carrito (temperatura) VALUES (%s);"
#         cursor.execute(query, (temperatura,))
#         conexion.commit()
#         cursor.close()
#         conexion.close()
#     except Exception as e:
#         print("Error al insertar en la base de datos:", e)

def batch_insert_temperatures(temperaturas):
    try:
        conexion = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conexion.cursor()
        query = "INSERT INTO carrito (temperatura) VALUES (%s)"
        cursor.executemany(query, temperaturas)
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error al insertar en la base de datos:", e)

# def read_temperature():
#     while True:
#         temperatura = bme280.get_temperature()
#         print('{:05.2f}*C'.format(temperatura))
#         insertar_temperatura(temperatura)
#         time.sleep(0.1)  # Adjust as needed

def read_temperature():
    temperature_readings = []
    batch_size = 5  # Number of readings to collect before batch insert

    while True:
        temperatura = bme280.get_temperature()
        temperature_readings.append((temperatura,))

        if len(temperature_readings) >= batch_size:
            batch_insert_temperatures(temperature_readings)
            temperature_readings = []  # Reset the list after batch insert

        time.sleep(0.1)  # Adjust as needed


#Rover------------------------------------
def insertar_distancia(distancia):
    try:
        conexion = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conexion.cursor()
        query = "INSERT INTO carrito (distancia) VALUES (%s);"
        cursor.execute(query, (distancia,))
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

# def read_distance():
#     sensor = DistanceSensor(echo=9, trigger=10)
#     while True:
#         cm = sensor.distance * 100
#         insertar_distancia(cm)  # Insertar distancia en la base de datos

#         if cm > 15:
#             start_forward()
#         else:
#             start_reverse()

#         time.sleep(0.1)  # Ajustar para mayor o menor sensibilidad

def read_distance():
    distance_readings = []
    batch_size = 5  # Number of readings to collect before batch insert

    sensor = DistanceSensor(echo=9, trigger=10)
    while True:
        cm = sensor.distance * 100
        distance_readings.append((cm,))

        if len(distance_readings) >= batch_size:
            batch_insert_distances(distance_readings)
            distance_readings = []  # Reset the list after batch insert

        # Rover control logic here
        if cm > 15:
            start_forward()
        else:
            start_reverse()

        time.sleep(0.1)  # Adjust as needed


def main():
    temperature_thread = threading.Thread(target=read_temperature)
    distance_thread = threading.Thread(target=read_distance)

    temperature_thread.start()
    distance_thread.start()

    temperature_thread.join()
    distance_thread.join()

if __name__ == '__main__':
    main()  


