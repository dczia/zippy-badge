import time
from os import urandom      # used for test random "audio" input
from rainbowio import colorwheel

from setup import pixels, num_pixels
from state import State
#from menu import menu_select, show_menu, show_select


class RaveState(State):

    @property
    def name(self):
        return "rave"

    def __init__(self):
        self.previous_intensity = 0
        self.mic_samples = bytearray(4)
        self.mic_samples_mv = memoryview(self.mic_samples)

    def enter(self, machine):
        # Show party mode text
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        self.mic_samples = urandom
        total = urandom(4)
        intensity = int(abs(total[0]))
        if intensity > 200:
            intensity = 200
        if (intensity > 0) and (intensity != self.previous_intensity):
            self.previous_intensity = intensity
            pixels.brightness = intensity/1000
            pixels.fill((0,0,255))
        pixels.show()
        time.sleep(0.05)