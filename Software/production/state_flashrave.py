import time

from ulab import numpy as np
from ulab.utils import spectrogram

from setup import pixels
from setup import mic
from state import State
from setup import keys
import global_tools


class FlashRaveState(State):

    @property
    def name(self):
        return "flashrave"

    def __init__(self):
        self.previous_intensity = 0
        self.volume = 0.5
        self.max = 1

    def enter(self, machine):
        pixels.fill((0, 0, 0))
        self.max_intensity = 0
        self.volume = 1
        self.previous_input = "none"
        self.running_max = 0
        self.running_min = 0
        self.exit_flag = False
        self.columnColor = 0
        State.enter(self, machine)

    def exit(self, machine):
        pixels.fill((0, 0, 0))
        pixels.show()
        State.exit(self, machine)

    def update(self, machine):
        columnColor = [
            (255, 0, 0),
            (255, 0, 115),
            (0, 0, 255),
            (0, 255, 0),
            (255, 255, 0),
            (155, 155, 155)
        ]

        # Poll for key press and cycle to next mode
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

                elif event.key_number == 2:
                    # right
                    if self.columnColor < len(columnColor) - 1:
                        self.columnColor += 1
                    else:
                        self.columnColor = 0
                elif event.key_number == 3:
                    # left
                    if self.columnColor == 0:
                        self.columnColor = len(columnColor) - 1
                    else:
                        self.columnColor -= 1

                elif event.key_number == 4:
                    if global_tools.current_brightness >= 0.05:
                        global_tools.current_brightness -= 0.05
                    else:
                        global_tools.current_brightness = 0.0
                    pixels.brightness = global_tools.current_brightness

        if self.exit_flag is True:
            machine.go_to_state("accel")

        else:
            try:
                # Get mic sample
                samples = np.array(
                    mic.read(block=True), dtype=np.int16
                )  # Record batch of 16-bit samples
                # Fix jankery due to mic by dropping even indexed samples
                samples = samples[1::2]

                # FFT
                spectrum = spectrogram(samples)

                # Log and binning to make cleaner, binning could be improved
                data = np.log(spectrum + 1e-7)
                data = np.interp(
                    np.arange(0, len(data), len(data) / 64, dtype=np.float),
                    np.arange(0, len(data), 1, dtype=np.uint16),
                    data,
                )

                bins = [data[12], data[12], data[12],
                        data[12], data[12], data[12]]

                # Calculate running max for auto_scaling
                self.running_max = (self.running_max * 24 + max(bins)) / 25
                self.running_min = (self.running_min * 24 + min(bins)) / 25

                # Fill pixels based on values
                pixels.fill((0, 0, 0))
                for index, item in enumerate(bins):
                    step = (self.running_max - self.running_min) / 7
                    if item > step + self.running_min:
                        pixels[(index) * 7] = columnColor[self.columnColor]
                    if item > step * 2 + self.running_min:
                        pixels[(index) * 7 + 1] = columnColor[self.columnColor]
                    if item > step * 3 + self.running_min:
                        pixels[(index) * 7 + 2] = columnColor[self.columnColor]
                    if item > step * 4 + self.running_min:
                        pixels[(index) * 7 + 3] = columnColor[self.columnColor]
                    if item > step * 5 + self.running_min:
                        pixels[(index) * 7 + 4] = columnColor[self.columnColor]
                    if item > step * 6 + self.running_min:
                        pixels[(index) * 7 + 5] = columnColor[self.columnColor]
                    if item > step * 7 + self.running_min:
                        pixels[(index) * 7 + 6] = columnColor[self.columnColor]
                pixels.show()
            except:
                pass
            time.sleep(0.05)
