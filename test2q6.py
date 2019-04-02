#!/usr/bin/env python3

import sys, time
import RPi.GPIO as GPIO

redPin = 11
greenPin = 13
bluePin = 15

GPIO.setwarnings(False)

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(redPin)

def greenOn():
    blink(greenPin)

def blueOn():
    blink(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def redOff():
    turnOff(redPin)

def greenOff():
    turnOff(greenPin)

def blueOff():
    turnOff(bluePin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)

def main():
    while True:
        cmd = raw_input("Input a color: ")
        if cmd == "red":
            whiteOff()
            redOn()
        elif cmd == "green":
            whiteOff()
            greenOn()
        elif cmd == "blue":
            whiteOff()
            blueOn()
        elif cmd == "yellow":
            whiteOff()
            yellowOn()
        elif cmd == "cyan":
            whiteOff()
            cyanOn()
        elif cmd == "magenta":
            whiteOff()
            magentaOn()
        elif cmd == "white":
            whiteOff()
            whiteOn()
        elif cmd == "quit":
            whiteOff()
            GPIO.cleanup()
            break
        else:
            print("Not a valid command")

    return

main()
