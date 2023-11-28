import RPi.GPIO as gpio
import time

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

def forward(sec):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False) 
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()

def reverse(sec):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True) 
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()

def turn_right(sec):
    init()
    # Activa solo los motores del lado izquierdo para girar a la derecha
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True) 
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()

def turn_left(sec):
    init()
    # Activa solo los motores del lado derecho para girar a la izquierda
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False) 
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()

print("forward")
forward(4)
print("turn right")
turn_right(2)
print("forward")
forward(4)
print("turn left")
turn_left(2)
print("reverse")
reverse(2)
