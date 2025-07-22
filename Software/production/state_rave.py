import time
import board

import ulab.numpy as np
import ulab.utils

from rainbowio import colorwheel

from setup import pixels, num_pixels
from setup import mic
from state import State
from setup import keys
#from menu import menu_select, show_menu, show_select


class RaveState(State):

    @property
    def name(self):
        return "rave"

    def __init__(self):
        self.previous_intensity = 0
        self.volume = .5
        self.max = 1

    def enter(self,machine):
        pixels.fill((0,0,0))
        self.max_intensity = 0
        self.volume = 1
        self.previous_input = "none"
        State.enter(self,machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        # Poll for key press and cycle to next mode
        event = keys.events.get()
        if event:
            if event.pressed:
                if event.key_number == 1:
                    machine.go_to_state("party")
        
        # Get audio sample
        data = np.array(mic.read(block=True), dtype = np.int16)

        # TODO:
        # Improve scaling
        # Make spectrogram using FFT
        # More color shifts based on sound

        # code for FFT
        #data = ulab.utils.spectrogram(data)
        #data = np.interp(
        #    np.arange(0, len(data), len(data) / 6, dtype=np.float),
        #    np.arange(0, len(data), 1, dtype=np.uint16),
        #    data
        #)

        # Scale audio sample and flash lights   
        intensity = int(abs(data[3])/self.volume)
        #print(intensity)
        if intensity > 200:
            intensity = 200
        if (intensity > 0) and (intensity != self.previous_intensity):
            self.previous_intensity = intensity

        pixels.brightness = (intensity-128)/2048
        pixels.fill((0,0,255))
        pixels.show()
        time.sleep(0.05)
        
