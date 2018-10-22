from nanpy import (ArduinoApi, SerialManager)
from time import sleep
import pyaudio
import sys
import numpy as np
import aubio

# setup pins
RED = 6
GREEN = 5
BLUE = 3
redValue = 0
greenValue = 0
blueValue = 0
delayTime = 1

# establish connection with the arduino
try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")

# set the pin colors
a.pinMode(RED, a.OUTPUT)
a.pinMode(GREEN, a.OUTPUT)
a.pinMode(BLUE, a.OUTPUT)

a.analogWrite(RED, redValue)
a.analogWrite(GREEN, greenValue)
a.analogWrite(BLUE, blueValue)

# init pyaudio
pyaudio_obj = pyaudio.PyAudio()

# open stream
CHUNK = 4000 # need 4000 for rpi
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = pyaudio_obj.open(format=pyaudio_format,
                          channels=n_channels,
                          rate=samplerate,
                          input=True,
                          frames_per_buffer=CHUNK)

if len(sys.argv) > 1:
    output_filename = sys.argv[1]
    record_duration = 5 # exit 1
    outputsink = aubio.sink(sys.argv[1], samplerate)
    total_frames = 0
else:
    # run
    outputsink = None
    record_duration = None

# get pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = CHUNK # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(tolerance)

print("starting recording:")
while True:
    try:
        audiobuffer = stream.read(CHUNK)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]

        print("{}".format(pitch))
        
        a.analogWrite(BLUE, blueValue)
        a.analogWrite(RED, redValue)
        a.analogWrite(GREEN, greenValue)
        #e ~82 yellow (255, 255, 0)
        #a ~110 green (0, 255, 255)
        #d ~147 blue (0, 0, 255)
        #g ~196 violet (231, 75, 231)
        #b ~246 red (255, 0, 0)
        #e ~329 orange (255, 165, 0)
        
        if pitch > 80 and pitch < 85: #e
            redValue = 255
            greenValue = 255
            blueValue = 0
        elif pitch > 104 and pitch < 115: #a
            redValue = 0
            greenValue = 255
            blueValue = 0
        elif pitch > 145 and pitch < 150: #d
            redValue = 0
            greenValue = 0
            blueValue = 255
        elif pitch > 193 and pitch < 199: #g
            redValue = 231
            greenValue = 75
            blueValue = 231
        elif pitch > 243 and pitch < 250: #b
            redValue = 255
            greenValue = 0
            blueValue = 0
        elif pitch > 326 and pitch < 335: #e
            redValue = 255
            greenValue = 165
            blueValue = 0
        else:
            redValue = redValue
            greenValue = greenValue
            blueValue = blueValue

        if outputsink:
            outputsink(signal, len(signal))

        if record_duration:
            totalframes += len(signal)
            if record_duration * samplerate < total_frames:
                break
    except KeyboardInterrupt:
        print("*** Exiting program")
        break

print("*** done...")
a.analogWrite(RED, a.LOW)
a.analogWrite(GREEN, a.LOW)
a.analogWrite(BLUE, a.LOW)
stream.stop_stream()
stream.close()
pyaudio_obj.terminate()







