from setup import pixels, num_pixels
from setup import keys
from setup import sensor
from state import State
#from menu import menu_select, show_menu, show_select


class AccelState(State):

    @property
    def name(self):
        return "accel"

    def enter(self, machine):
        pixels.fill((0,0,0))
        
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

        # Light leds based on tilt
        pixels.fill((0,0,0))
        if abs(acc_x) > abs (acc_y):
            if acc_x > 0:
                for led in range(35,42):
                    pixels[led] = (0,0,255)
            else:
                for led in range(0,7):
                    pixels[led] = (0,0,255)

        else:
            if acc_y > 0:
                for led in range(0,6):
                    pixels[led*7] = (0,0,255)
            else:
               for led in range(0,6):
                    pixels[led*7+6] = (0,0,255)
        pixels.show()
 
