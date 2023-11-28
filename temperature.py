import time
import mysql.connector
from smbus2 import SMBus
from bme280 import BME280

# Configuración de la conexión a la base de datos MySQL
db_host = "retocarritocloud.czosggbj7hr7.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "8ik9FiE2AgE*tu_tabla"
db_name = "micarrito"

# Función para insertar la temperatura en la base de datos
def insertar_temperatura(temperatura):
    try:
        conexion = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        cursor = conexion.cursor()
        query = "INSERT INTO carrito (temperatura) VALUES (%s);"
        cursor.execute(query, (temperatura,))
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        print("Error al insertar en la base de datos:", e)

# Configuración del sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

while True:
    temperatura = bme280.get_temperature()
    print('{:05.2f}*C'.format(temperatura))

    # Insertar la temperatura en la base de datos
    insertar_temperatura(temperatura)

    # Espera antes de leer el siguiente valor (por ejemplo, 60 segundos)
    time.sleep(0.1)
