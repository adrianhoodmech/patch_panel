#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pygame
import numpy as np
import os

ledPins = [7,11,13,15]
keyPins = [8,10,12,16]

keys = len(keyPins)
rows = m = 2
cols = n = 2

ON = 0
OFF = 1

z = [1] * m * n
panelState = np.copy(z)
lastState = np.copy(z)

beatsPerMin = 100.
stepTime = 60. / beatsPerMin             # seconds until next step
position = 0

ResetTime   = 10*60
fx_sounds   = []
fxVolume    = 100

dir_path = os.path.dirname(os.path.realpath(__file__))      # returns the directory of this file

def killAudio():
    pygame.mixer.quit()

def initAudio():
    # PyGame Initialization
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.mixer.init()
    #pygame.mixer.set_num_channels(20)

    global fx_sounds
    fx_sounds = [

        pygame.mixer.Sound(dir_path + '/samples/a.wav'),
        pygame.mixer.Sound(dir_path + '/samples/d.wav'),

        pygame.mixer.Sound(dir_path + '/samples/b.wav'),
        pygame.mixer.Sound(dir_path + '/samples/d.wav')]

    for sound in fx_sounds:
        sound.set_volume(fxVolume)

def initGpio():                         # GPIO Initialization
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for key in keyPins:                  # set all the columns as outputs FOR TESTING
        #print(key)
        GPIO.setup(keyPins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for led in ledPins:
        GPIO.setup(ledPins, GPIO.OUT)
    print("GPIO setup.")

def scanKey():                                  # define scan functions
    here=0                                     # resets index; scans through the rows and columns one time
    for key in keyPins:
        keyState = GPIO.input(key)            # test each key

        if lastState[here] != keyState:   # check key state
            time.sleep(.050)              # bounce behavior too irregular for counter; use timed debounce instead
            lastState[here] = keyState

            if ((panelState[here] == OFF) and (keyState == ON)):                # A key's turned on,
                print(here," ON")
                panelState[here] = ON            # activate spot in panel state
                GPIO.output(ledPins[here],1)    # turn light on
                #pygame.mixer.find_channel(True).play(fx_sounds[here])

            elif ((panelState[here] == ON) and (keyState == ON)):                # A key's turned off,
                print(here," OFF")
                panelState[here] = OFF            # deactivate spot in panel state
                GPIO.output(ledPins[here],0)    # turn light on
                #pygame.mixer.find_channel(True).play(fx_sounds[here])

        here = here + 1           # increments index

def seqRun(c):
    for row in range(rows):
        buttDial = c*rows + row
        if panelState[buttDial] == ON:
            print("Play", buttDial)
            pygame.mixer.find_channel(True).play(fx_sounds[buttDial])       # plays sound on open channel, up to 20

while True:
    try:
        initAudio()                            # start up stuff
        pygame.init()
        initGpio()

        # Timestamp for Buffer Clearing
        endTime = time.time() + ResetTime

        while (time.time() < endTime):              # reset pygame after countdown
            nextStep = time.time() + stepTime           # prepare next beat
            seqRun(position)                            # play sounds
            position = (position + 1) % n               # advance count to next column
            #print(nextStep)
            while (time.time() < nextStep):
                scanKey()                                # scans key(s)

    finally:
        pygame.quit()
        pygame.mixer.quit()
