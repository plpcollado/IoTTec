import RPi.GPIO as GPIO
import time
import threading
import mysql.connector
from smbus2 import SMBus
from bme280 import BME280
from gpiozero import DistanceSensor

# Configuración de la base de datos MySQL
db_host = "retocarritocloud.czosggbj7hr7.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "8ik9FiE2AgE*"  # Cambiar por tu contraseña real
db_name = "micarrito"

# Función para insertar datos en la base de datos
def insertar_datos(tabla, valor):
    try:
        conexion = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conexion.cursor()
        query = f"INSERT INTO {tabla} (valor) VALUES (%s);"
        cursor.execute(query, (valor,))
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error al insertar en la base de datos:", e)

def read_temperature():
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)
    while True:
        temperatura = bme280.get_temperature()
        print('{:05.2f}*C'.format(temperatura))
        insertar_datos("carrito", temperatura)
        time.sleep(0.1)

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

# Funciones start_forward, start_reverse y stop van aquí...
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
        insertar_datos("distancia", cm)
        if cm > 15:
            start_forward()
        else:
            start_reverse()
        time.sleep(0.1)

def main():
    temperature_thread = threading.Thread(target=read_temperature)
    distance_thread = threading.Thread(target=read_distance)

    temperature_thread.start()
    distance_thread.start()

    temperature_thread.join()
    distance_thread.join()

if __name__ == '__main__':
    main()