#!/usr/bin/python

import sox

while True:
    sox -t alsa plughw:1 -d
    