import time

from ulab import numpy as np
from ulab.utils import spectrogram

from setup import pixels
from setup import mic
from state import State
from setup import keys
from setup import current_brightness


class RaveState(State):

    @property
    def name(self):
        return "rave"

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
        self.brightness = current_brightness
        self.exit_flag = False
        State.enter(self, machine)

    def exit(self, machine):
        global current_brightness
        current_brightness = self.brightness
        pixels.fill((0, 0, 0))
        pixels.show()
        State.exit(self, machine)

    def update(self, machine):
        # Poll for key press and cycle to next mode
        event = keys.events.get()
        if event:
            if event.pressed:
                if event.key_number == 1:
                    self.exit_flag = True
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

        # Adding to smooth the transition between modes
        if self.exit_flag is True:
            machine.go_to_state("scroll_text")
        
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

                bins = [data[12], data[10], data[8], data[7], data[4], data[1]]

                # Calculate running max for auto_scaling
                self.running_max = (self.running_max * 24 + max(bins)) / 25
                self.running_min = (self.running_min * 24 + min(bins)) / 25

                # Fill pixels based on values
                pixels.fill((0, 0, 0))
                column = [
                    (255, 0, 0),
                    (255, 0, 0),
                    (192, 0, 64),
                    (128, 0, 128),
                    (64, 0, 192),
                    (0, 0, 255),
                    (0, 0, 255),
                ]
                for index, item in enumerate(bins):
                    step = (self.running_max - self.running_min) / 7
                    if item > step + self.running_min:
                        pixels[(index) * 7] = column[6]
                    if item > step * 2 + self.running_min:
                        pixels[(index) * 7 + 1] = column[5]
                    if item > step * 3 + self.running_min:
                        pixels[(index) * 7 + 2] = column[4]
                    if item > step * 4 + self.running_min:
                        pixels[(index) * 7 + 3] = column[3]
                    if item > step * 5 + self.running_min:
                        pixels[(index) * 7 + 4] = column[2]
                    if item > step * 6 + self.running_min:
                        pixels[(index) * 7 + 5] = column[1]
                    if item > step * 7 + self.running_min:
                        pixels[(index) * 7 + 6] = column[0]
                pixels.show()
            except:
                pass
            time.sleep(0.05)
