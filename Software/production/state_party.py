import time
from rainbowio import colorwheel

from setup import pixels, num_pixels
from setup import keys
from state import State
import global_tools

# from menu import menu_select, show_menu, show_select


class PartyState(State):

    @property
    def name(self):
        return "party"

    def enter(self, machine):
        self.exit_flag = False
        State.enter(self, machine)

    def exit(self, machine):
        pixels.fill((0,0,0))
        pixels.show()
        State.exit(self, machine)

    def update(self, machine):
        for j in range(255):
            for i in range(num_pixels):
                rc_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(rc_index & 255)

                # Check for keypress in loop for prompt changes
                event = keys.events.get()
                if event:
                    if event.pressed:
                        if event.key_number == 1:
                            self.exit_flag = True

                        # Brightness controls
                        elif event.key_number == 0:
                            if global_tools.current_brightness <= 0.45:
                                global_tools.current_brightness += 0.05
                            else:
                                global_tools.current_brightness = 0.5
                            pixels.brightness = global_tools.current_brightness

                        elif event.key_number == 4:
                            if global_tools.current_brightness >= 0.05:
                                global_tools.current_brightness -= 0.05
                            else:
                                global_tools.current_brightness = 0.0
                            pixels.brightness = global_tools.current_brightness

            if self.exit_flag is True:
                machine.go_to_state("accel")
                break
            else:
                pixels.show()
