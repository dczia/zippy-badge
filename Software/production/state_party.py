import time

from rainbowio import colorwheel

from setup import pixels, num_pixels
from state import State
#from menu import menu_select, show_menu, show_select


class PartyState(State):

    @property
    def name(self):
        return "party"

    def __init__(self):
        self.total_lines = 10

    def enter(self, machine):
        # Show party mode text
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        for j in range(255):
            for i in range(num_pixels):
                rc_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(rc_index & 255)
            pixels.show()
            #time.sleep(0)

