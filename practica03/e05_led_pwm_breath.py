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
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)

## Canales múltiples
# Hay que establecer cada canal utilizado como entrada o salida
# list_name = [x,x,x]
# GPIO.setup(list_name, GPIO.IN or GPIO.OUT, initial=GPIO.LOW or GPIO.HIGH)

## PWM ##
led_pwm = GPIO.PWM(12, 50) # (channel, frequency MHz)
led_pwm.start(0) # (ducy_cycle)

def led_pwm_tiempo():
    for dc in range (0, 101, 9): # 0 <= dc <= 100 ; con saltos de 9
        led_pwm.ChangeDutyCycle(dc)
        sleep(0.1)
    sleep(0.5)
    for dc in range (100, -1, -9): # 0 <= dc <= 100 ; con saltos de 9
        led_pwm.ChangeDutyCycle(dc)
        sleep(0.1)

### MAIN ###

while True: # Bucle infinito
    led_pwm_tiempo()