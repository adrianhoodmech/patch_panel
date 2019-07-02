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

z = [1] * m * n
panelState = np.copy(z)
lastState = np.copy(z)

stepTime = 1          # milliseconds
bounce_limit = 1
count = 0

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
        GPIO.setup(keyPins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for led in ledPins:
        GPIO.setup(ledPins, GPIO.OUT)
    print("GPIO setup.")

def scanKey():                                  # define scan functions
    here=0                                     # resets index; scans through the rows and columns one time
    for key in keyPins:
        bounce_count = 0
        keyState = GPIO.input(key)            # test each key

        if lastState[here] != keyState:   # check key state
            bounce_count = bounce_count + 1     # counts the number of key bounces

            if bounce_count >= bounce_limit:    # after debounce satisfied, record key state
                print(bounce_count)
                bounce_count = 0                # reset bounce counter
                lastState[here] = keyState

                if keyState == 0:                # A key's been pressed,
                    print(here," ON")
                    panelState[here] = 0            # activate spot in panel state
                    #GPIO.output(ledPins[here],1)    # turn light on
                    pygame.mixer.find_channel(True).play(fx_sounds[here])
                else:
                    print(here," OFF")
                    panelState[here] = 1
                    #GPIO.output(ledPins[here],0)
                    pygame.mixer.find_channel(True).play(fx_sounds[here])

        else:
            bounce_count = 0         # records 0 if no key state change
        here = here + 1           # increments index

def seqRun(count):
    for row in range(rows):
        index = count*rows + row
        #print(index)
        if panelState[index] == 0:
            #fx_sounds[index].play()
            print("Play", index)
            pygame.mixer.find_channel(True).play(fx_sounds[index])


while True:                                     # MAIN LOOP
    try:
        initAudio()                            # start up stuff
        pygame.init()
        initGpio()

        # Timestamp for Buffer Clearing
        endTime = time.time() + ResetTime

        while (time.time() < endTime):              # reset pygame after countdown
            seqRun(count)                                # play the pretty noises
            count = (count + 1) % n
            nextStep = time.time() + stepTime           # ready for the next beat
            #print(nextStep)
            while (time.time() < nextStep):
                scanKey()                                # scan through the key(s) looking for input

    finally:
        pygame.quit()
        pygame.mixer.quit()
