import time
from rainbowio import colorwheel

from setup import pixels, num_pixels
from setup import keys
from setup import current_brightness
from state import State

# from menu import menu_select, show_menu, show_select


class PartyState(State):

    @property
    def name(self):
        return "party"

    def enter(self, machine):
        self.brightness = current_brightness
        State.enter(self, machine)

    def exit(self, machine):
        current_brightness = self.brightness
        State.exit(self, machine)

    def update(self, machine):

        # pixels.brightness = 0.1
        for j in range(255):
            for i in range(num_pixels):
                rc_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(rc_index & 255)
                event = keys.events.get()
                if event:
                    if event.pressed:
                        if event.key_number == 1:
                            machine.go_to_state("accel")

                    # Brightness controls
                    elif event.key_number == 0:
                        if self.brightness <= 0.5:
                            self.brightness += 0.05
                            pixels.brightness = self.brightness
                    elif event.key_number == 4:
                        if self.brightness >= 0.05:
                            self.brightness -= 0.05
                        else:
                            self.brightness = 0.0
                        pixels.brightness = self.brightness

            pixels.show()
            time.sleep(0)
