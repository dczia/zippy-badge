from setup import pixels, num_pixels
from setup import keys
from setup import sensor
from state import State
from rainbowio import colorwheel
#from menu import menu_select, show_menu, show_select


class AccelState(State):

    @property
    def name(self):
        return "accel"

    def __init__(self):
        self.hue = 0
        self.target_hue = 0

    def enter(self, machine):
        pixels.fill((0,0,0))
        pixels.brightness = 0.1
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        # Check for button press
        event = keys.events.get()
        if event:
            if event.pressed:
                if event.key_number == 1:
                    machine.go_to_state("rave")

        # Get accelerometer data
        acc_x, acc_y, acc_z = sensor.acceleration

        # Set target hue based on tilt direction
        if abs(acc_x) > abs(acc_y):
            if acc_x > 0:  # Tilted right
                self.target_hue = 0  # Red
            else:  # Tilted left
                self.target_hue = 85  # Green
        else:
            if acc_y > 0:  # Tilted forward
                self.target_hue = 170  # Blue
            else:  # Tilted back
                self.target_hue = 255  # Purple

        # Smooth fade towards target hue
        if self.hue != self.target_hue:
            if self.hue < self.target_hue:
                if self.target_hue - self.hue > 128:
                    self.hue = (self.hue - 1) % 256
                else:
                    self.hue = (self.hue + 1) % 256
            else:
                if self.hue - self.target_hue > 128:
                    self.hue = (self.hue + 1) % 256
                else:
                    self.hue = (self.hue - 1) % 256

        # Get the current color
        color = colorwheel(self.hue)

        # Fill the entire LED grid with the color
        pixels.fill(color)
        pixels.show()
 
