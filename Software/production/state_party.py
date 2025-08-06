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

    def __init__(self):
        super().__init__()
        self.pattern_index = 0
        self.j = 0

    def enter(self, machine):
        self.brightness = current_brightness
        State.enter(self, machine)

    def exit(self, machine):
        current_brightness = self.brightness
        State.exit(self, machine)

    def update(self, machine):
        pattern_count = 3
        
        # Check for button presses
        event = keys.events.get()
        if event and event.pressed:
            if event.key_number == 1:
                machine.go_to_state("accel")
                return
            # Next pattern
            elif event.key_number == 2:
                self.pattern_index = (self.pattern_index + 1) % pattern_count
            # Previous pattern
            elif event.key_number == 3:
                self.pattern_index = (self.pattern_index - 1) % pattern_count
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

        # Pattern 0: Classic rainbow
        if self.pattern_index == 0:
            for i in range(num_pixels):
                rc_index = (i * 256 // num_pixels) + self.j
                pixels[i] = colorwheel(rc_index & 255)

        # Pattern 1: Rainbow pulse
        elif self.pattern_index == 1:
            # Simple outward-moving rainbow pulse
            for i in range(num_pixels):
                # Create a color index that changes based on position and time
                color_index = ((i * 8) + self.j) & 255
                pixels[i] = colorwheel(color_index)

        # Pattern 2: Rainbow wave
        elif self.pattern_index == 2:
            center = num_pixels // 2
            for i in range(num_pixels):
                distance = abs(i - center)
                rc_index = (distance * 8 + self.j * 3) & 255
                pixels[i] = colorwheel(rc_index)

        pixels.show()
        time.sleep(0.02)  # Slightly slower for smoother animation
        self.j = (self.j + 1) % 255
