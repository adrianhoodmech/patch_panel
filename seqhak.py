#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pygame
import numpy as np
import os

keyPins = [3,5,7,11]
ledPins = [8,10,12,16]

keys = len(keyPins)
rows = m = 2
cols = n = 2

z = [0] * m * n
panelState = np.copy(z)
lastState = np.copy(z)

stepTime = 350          # milliseconds
bounce_limit = 3
i = 0

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
    pygame.mixer.set_num_channels(20)

    global fx_sounds
    fx_sounds = [

        pygame.mixer.Sound(dir_path + '/samples/a.wav'),
        pygame.mixer.Sound(dir_path + '/samples/b.wav'),

        pygame.mixer.Sound(dir_path + '/samples/c.wav'),
        pygame.mixer.Sound(dir_path + '/samples/d.wav')
,    ]

    for sound in fx_sounds:
        sound.set_volume(fxVolume)

def initGpio():                         # GPIO Initialization
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for key in keyPins:                  # set all the columns as outputs FOR TESTING
        print(key)
        GPIO.setup(keyPins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for led in ledPins:
        GPIO.setup(ledPins, GPIO.OUT)
    print("GPIO setup.")

def scanKey():                                  # define scan function
    here=0                                     # resets index; scans through the rows and columns one time
    for key in keyPins:
        bounce_count = 0
        keyState = GPIO.input(key)            # test each key

        if lastState[here] != keyState:   # check key state
            bounce_count = bounce_count + 1     # counts the number of key bounces

            if bounce_count >= bounce_limit:    # after debounce satisfied, record key state
                bounce_count = 0                # reset bounce counter
                lastState[here] = keyState

                if keyState == 1:                # A key's been pressed,
                    panelState[here] = 1            # activate spot in panel state
                    GPIO.output(ledPins[here],1)    # turn light on
                    pygame.mixer.find_channel(True).play(fx_sounds[here])
                else:
                    panelState[here] = 0
                    GPIO.output(ledPins[here],0)
                    pygame.mixer.find_channel(True).play(fx_sounds[here])
        else:
            bounce_count[here] = 0         # records 0 if no key state change
        here = here + 1           # increments index

def seqRun():
    for row in range(rows):
        index = i*rows + row
        if panelState[index] == 1:
            #fx_sounds[index].play()
            pygame.mixer.find_channel(True).play(fx_sounds[index])
    i = (i + 1) % n

while True:                                     # MAIN LOOP
    try:
        initAudio()                            # start up stuff
        pygame.init()
        initGpio()

        # Timestamp for Buffer Clearing
        endTime = time.time() + ResetTime

        while (time.time() < endTime):              # reset pygame after countdown
            seqRun()                                # play the pretty noises
            nextStep = time.time() + stepTime           # ready for the next beat
            while (time.time() < nextStep):
                scanKey()                                # scan through the key(s) looking for input

    finally:
        pygame.quit()
        pygame.mixer.quit()
