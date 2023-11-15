from gpiozero import DistanceSensor
from time import sleep

#sensor.close()
sensor = DistanceSensor(echo=9, trigger=10)


while True:
    cm = sensor.distance * 100
    inch = cm / 2.5
    print("cm={:.0f} inch={:.0f}".format(cm, inch))
    sleep(0.5)