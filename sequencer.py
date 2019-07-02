#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pygame
import numpy
import os

rowPins = [8,10]
colPins = [3,5,7,11]
ledPins = [7,8,9,10,11,12,13,14]

rows = m = len(rowPins)
cols = n = len(colPins)

z = [0] * m * n
panelState = z.copy()
lastState = z.copy()

stepTime = 250          # milliseconds
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

        pygame.mixer.Sound(dir_path + 'a.wav'),
        pygame.mixer.Sound(dir_path + 'b.wav'),

        pygame.mixer.Sound(dir_path + 'a.wav'),
        pygame.mixer.Sound(dir_path + 'b.wav'),

        pygame.mixer.Sound(dir_path + 'a.wav'),
        pygame.mixer.Sound(dir_path + 'b.wav'),

        pygame.mixer.Sound(dir_path + 'a.wav'),
        pygame.mixer.Sound(dir_path + 'b.wav')
    ]

    for sound in fx_sounds:
        sound.set_volume(fxVolume)

def initGpio():                         # GPIO Initialization
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for row in rowPins:                 # set all the rows as pull down inputs
        print(row)
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for col in cols:                  # set all the columns as outputs FOR TESTING
        print(col)
        GPIO.setup(colPins, GPIO.OUT)

    for led in ledPins
        GPIO.setup(ledPins, GPIO.OUT)
    print("GPIO setup.")

def scanKey():                                  # define scan function
    here=0                                     # resets index; scans through the rows and columns one time
    for col in cols:
        for row in rows:
            bounce_count = 0
            keyState = GPIO.input(row)            # test each row in each column

            if lastState[here] != keyState:   # check key state
                bounce_count = bounce_count + 1     # counts the number of key bounces

                if bounce_count >= bounce_limit:    # after debounce satisfied, record key state
                    bounce_count = 0                # reset bounce counter
                    lastState[here] = keyState

                    if keyState == 1:                # A key's been pressed,
                        panelState[here] = 1            # activate spot in panel state
                        GPIO.output(ledPins[here],1)    # turn light on
                        # play sound?
                        # fx_sounds[index].play()
                    else:
                        panelState[here] = 0
                        GPIO.output(ledPins[here],0)
                        # play sound?
                        # fx_sounds[index].play()
                        # activate spot in panel state
                        #panelState(here) = 0

            else:
                bounce_count[index] = 0         # records 0 if no key state change
            index = index + 1           # increments index

        GPIO.output(col, 0)             # turn the column off and move on to the next column

def seqRun():
   for key in range(rows)
        index = i*rows + key
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
