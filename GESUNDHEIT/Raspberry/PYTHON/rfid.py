import RPi.GPIO as GPIO
import
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    while True:
        
        option = input("Lesen (r) oder Schreiben (w)?")

        if option.lower() == "r":
            id, data = reader.read()
            print(id)
            print(data)

        else:
            text = input("Daten eingeben: ")
            reader.write(text)
            print(f"Ok. Text geschrieben: ")

finally:
    GPIO.cleanup()