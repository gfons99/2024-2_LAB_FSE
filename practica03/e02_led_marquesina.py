# author: F.R., G.M.
# title: Ejercicio 02. Marquesina de LEDs de izquierda a derecha
# date: 2024-03-02

### RPi.GPIO module basics ###
import RPi.GPIO as GPIO
from time import sleep

## Pin Numbering
# Opción 1: Funciona en cualquier versión de tarjeta Raspberry Pi sin necesidad de cambiar las conexiones
GPIO.setmode(GPIO.BOARD)
# Opción 2: Requiere cambiar las conexiones dependiendo de la versión de tarjeta Raspberry Pi
#GPIO.setmode(GPIO.BCM)

## Warnings
# Es preferible deshabilitarlas al usar más de un script/circuito con GPIO
GPIO.setwarnings(False)

## Canales simples
# Hay que establecer cada canal utilizado como entrada o salida
# GPIO.setup(channel, GPIO.IN or GPIO.OUT, initial=GPIO.LOW or GPIO.HIGH)

## Canales múltiples
# Hay que establecer cada canal utilizado como entrada o salida
led7_list = [12,16,18,22,24,26,32]
GPIO.setup(led7_list, GPIO.OUT, initial=GPIO.LOW)

state_tuple = (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.LOW,GPIO.LOW)

def marquesina():
    global led7_list
    global state_tuple
    GPIO.output(led7_list, state_tuple)
    state_tuple = state_tuple[-1:] + state_tuple[:-1]

### MAIN ###
while True: # Bucle infinito
	sleep(0.5) # segundos
	marquesina()