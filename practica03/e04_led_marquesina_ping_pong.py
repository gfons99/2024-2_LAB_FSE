# author: F.R., G.M.
# title: Ejercicio 02. Marquesina de LEDs de izquierda a derecha
# date: 2024-03-02

### RPi.GPIO module basics ###
import RPi.GPIO as GPIO
from time import sleep
import threading

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
tiempo_s = 0.2
direccion = 0
def tiempo_usuario():
    global tiempo_s
    while True:
        tiempo_s = float(input("Ingrese el tiempo en segundos (puede usar decimales):"))

def marquesina():
    global led7_list
    global state_tuple
    global direccion

    GPIO.output(led7_list, state_tuple)
    # Cambio de bandera
    if(state_tuple[0] == GPIO.HIGH):
        direccion = 0
    if (state_tuple[-1] == GPIO.HIGH):
        direccion = 1
    # Cambio de dirección
    if (direccion == 0):
        state_tuple = state_tuple[-1:] + state_tuple[:-1]   # izq - der
    else:
        state_tuple = state_tuple[1:] + state_tuple[:1]     # der - izq

### MAIN ###
tiempo_thread = threading.Thread(target=tiempo_usuario)
tiempo_thread.daemon = True
tiempo_thread.start()

while True: # Bucle infinito
    sleep(tiempo_s)
    marquesina()