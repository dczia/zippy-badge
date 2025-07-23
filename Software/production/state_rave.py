import time
import board

from array import array
from math import log
from time import monotonic
from supervisor import reload
import board
from rainbowio import colorwheel
from ulab import numpy as np
from ulab.utils import spectrogram

from setup import pixels, num_pixels
from setup import mic
from state import State
from setup import keys
#from menu import menu_select, show_menu, show_select


def led_array(pixels, column, row, color):
    try:
        pixel_index = (5-column)*7 + (6-row)
        pixels[pixel_index] = color
    except:
        pass
        #print(f"Failed index\n")
        #print(f"Row: {row}\n")
        #print(f"Column: {column}\n")
        #print(f"Index: {pixel_index}\n")
    return


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
        pixels.brightness = .05
        self.max_intensity = 0
        self.volume = 1
        self.previous_input = "none"
        self.running_max = 0
        self.running_min = 0
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
        

        try:
            # Get mic sample
            samples = np.array(mic.read(block=True), dtype = np.int16) # Record batch of 16-bit samples
            # Fix jankery due to mic by dropping even indexed samples
            samples = samples[1::2]

            # FFT
            spectrum = spectrogram(samples)

            # Log and binning to make cleaner, binning could be improved
            data = np.log(spectrum + 1e-7)
            data = np.interp(
                np.arange(0, len(data), len(data) / 64, dtype=np.float),
                np.arange(0, len(data), 1, dtype=np.uint16),
                data
            )



            #bins = [data[0],data[1],data[8],data[10],data[12],data[14]]
            bins = [data[14],data[12],data[10],data[8],data[1],data[0]]

            self.running_max = (self.running_max * 4 + max(bins))/5
            self.running_min = (self.running_min * 4 + min(bins))/5

            print(f"Bins: {bins}\n")
            print(f"Max: {self.running_max}\n")
            print(f"Min: {self.running_min}\n")

            pixels.fill((0,0,0))
            column = [(255,0,0),(255,0,0),(192,0,64),(128,0,128),(64,0,192),(0,0,255),(0,0,255)]
            pixels.fill((0,0,0))
            for index,item in enumerate(bins):
                if index > -1 and index < 13 :
                    #index -= 7
                    step = (self.running_max-self.running_min)/6
                    pixels[(index) * 7] = column[6]
                    if item > step + self.running_min:
                        pixels[(index) * 7 + 1] = column[5]
                    if item > step*2 + self.running_min:
                        pixels[(index) * 7 + 2] = column[4]
                    if item > step*3 + self.running_min:
                        pixels[(index) * 7 + 3] = column[3]
                    if item > step*4 + self.running_min:
                        pixels[(index) * 7 + 4] = column[2]
                    if item > step*5 + self.running_min:
                        pixels[(index) * 7 + 5] = column[1]
                    if item > step*6 + self.running_min:
                        pixels[(index) * 7 + 6] = column[0]
            pixels.show()
            time.sleep(0.05)
        except:
            pass  