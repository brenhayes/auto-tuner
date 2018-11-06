from nanpy import ArduinoApi, SerialManager, Stepper
from time import sleep
print("hello")
try:
    connection = SerialManager()
    a = ArduinoApi(connection=connection)
except:
    print("connection failed")

print("hello two")
# Number of steps per revolution
stepsPerRevolution = 1500
# Initialize Stepper library on pins 8 through 11
print(stepsPerRevolution, "Steps per rev")
myStepper = Stepper(revsteps=stepsPerRevolution, pin1=8, pin2=10, pin3=9, pin4=11)
myStepper.setSpeed(20)
print("breakpoint")
while True:
    print("clockwise")
    myStepper.step(stepsPerRevolution)
    sleep(1000)

    print("counter clockwise")
    myStepper.step(-stepsPerRevolution)
    sleep(1000)

