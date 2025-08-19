from setup import pixels, num_pixels
from setup import keys
from setup import sensor
from state import State
from rainbowio import colorwheel
import global_tools

# from menu import menu_select, show_menu, show_select


class AccelState(State):

    @property
    def name(self):
        return "accel"

    def __init__(self):
        self.hue = 0
        self.target_hue = 0
        self.pattern_index = 0
        self.trail_positions = [0] * 8  # For pattern 2
        self.wave_offset = 0  # For pattern 3

    def enter(self, machine):
        self.exit_flag = False
        State.enter(self, machine)

    def exit(self, machine):
        pixels.fill((0, 0, 0))
        pixels.show()
        State.exit(self, machine)

    def update(self, machine):
        pattern_count = 3
        # Check for button press
        event = keys.events.get()
        if event:
            if event.pressed:
                if event.key_number == 1:
                    self.exit_flag = True

                # Next pattern
                elif event.key_number == 2:
                    self.pattern_index = (
                        self.pattern_index + 1) % pattern_count
                # Previous pattern
                elif event.key_number == 3:
                    self.pattern_index = (
                        self.pattern_index - 1) % pattern_count

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
            machine.go_to_state("party")

        else:
            # Get accelerometer data
            acc_x, acc_y, acc_z = sensor.acceleration

            if self.pattern_index == 0:
                # Pattern 0: Original color direction pattern
                if abs(acc_z) > 3:  # Significant vertical movement
                    if acc_z > 0:  # Moving up
                        self.target_hue = 42  # Orange
                    else:  # Moving down
                        self.target_hue = 128  # Cyan
                elif abs(acc_x) > abs(acc_y):
                    if acc_x > 0:  # Tilted right
                        self.target_hue = 0  # Red
                    else:  # Tilted left
                        self.target_hue = 85  # Green
                else:
                    if acc_y > 0:  # Tilted forward
                        self.target_hue = 170  # Blue
                    else:  # Tilted back
                        self.target_hue = 255  # Purple

            elif self.pattern_index == 1:
                # Pattern 1: Intensity-based pattern
                # Use total acceleration to determine color intensity
                total_acc = (acc_x ** 2 + acc_y ** 2 + acc_z ** 2) ** 0.5
                # More movement = more color change
                self.target_hue = int((total_acc * 20) % 256)

            elif self.pattern_index == 2:
                # Pattern 2: Tilt Level Meter
                # Move colors based on tilt angle
                # Convert tilt to pixel position
                tilt_x = int((acc_x + 10) * (num_pixels/20))
                # Constrain to valid pixel range
                tilt_x = max(0, min(num_pixels-1, tilt_x))

                # Update trail positions
                self.trail_positions = [tilt_x] + self.trail_positions[:-1]

                # Clear pixels
                pixels.fill((0, 0, 0))

                # Draw trail with fading colors
                for i, pos in enumerate(self.trail_positions):
                    if 0 <= pos < num_pixels:
                        color = colorwheel((self.hue + i * 30) % 256)
                        pixels[pos] = color

                # Skip the normal color fill
                pixels.show()
                self.hue = (self.hue + 1) % 256
                return

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
