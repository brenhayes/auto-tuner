from nanpy import ArduinoApi, SerialManager, Stepper
from time import sleep

connection = SerialManager()
a = ArduinoApi(connection=connection)

# Number of steps per revolution
stepsPerRevolution = 1500
# Initialize Stepper library on pins 8 through 11
myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11)
myStepper.setSpeed(20)

while True:
    print("clockwise")
    myStepper.step(stepsPerRevolution)
    sleep(1000)

    print("counter clockwise")
    myStepper.step(-stepsPerRevolution)
    sleep(1000)
