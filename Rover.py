import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import threading
import mysql.connector

# Configuración de la base de datos MySQL
db_host = "retocarritocloud.czosggbj7hr7.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "8ik9FiE2AgE*"  # Cambiar por tu contraseña real
db_name = "micarrito"

# Función para insertar la distancia en la base de datos
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

def read_distance():
    sensor = DistanceSensor(echo=9, trigger=10)
    while True:
        cm = sensor.distance * 100
        insertar_distancia(cm)  # Insertar distancia en la base de datos

        if cm > 15:
            start_forward()
        else:
            start_reverse()

        time.sleep(0.1)  # Ajustar para mayor o menor sensibilidad


def main():
    distance_thread = threading.Thread(target=read_distance)
    distance_thread.start()

    # You can add more threads if needed for other tasks

if __name__ == '__main__':
    main()  