from setup import pixels
from setup import keys
from setup import sensor
from state import State

import fontio
import time
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel
from setup import current_brightness


class ScrollState(State):

    @property
    def name(self):
        return "scroll_text"

    def __init__(self):
        self.hue = 0
        self.target_hue = 0

    def enter(self, machine):

        # Most of this is for scrolling text and can be moved if we use it anywhere else
        # Putting it here for now to make this work quickly
        tom_thumb = bitmap_font.load_font("tom-thumb.pcf", Bitmap)

        _glyph_keys = [
            "bitmap",
            "tile_index",
            "width",
            "height",
            "dx",
            "dy",
            "shift_x",
            "shift_y",
        ]

        def patch_glyph(base, **kw):
            d = {}
            for k in _glyph_keys:
                d[k] = kw.get(k, getattr(base, k))
            return fontio.Glyph(**d)

        class PatchedFont:
            def __init__(self, base_font, patches):
                self.base_font = base_font
                self.patches = patches

            def get_glyph(self, glyph):
                g = self.base_font.get_glyph(glyph)
                patch = self.patches.get(glyph)
                if patch is not None:
                    # print("patching", repr(chr(glyph)), g)
                    g = patch_glyph(g, **patch)
                    # print("patched", g)
                return g

            def get_bounding_box(self):
                return self.base_font.get_bounding_box()

        self.font = PatchedFont(
            tom_thumb,
            {
                32: {"shift_x": 1, "dx": 0},
                105: {"dx": 0, "shift_x": 2},
                33: {"dx": 0, "shift_x": 2},
            },
        )

        # Create a label object
        self.label = Label(text="text", font=self.font)
        self.bitmap = self.label.bitmap

        self.hue = 0
        self.label.text = "    DCZIA    "
        self.bitmap = self.label.bitmap
        self.brightness = current_brightness
        self.go_next = False
        self.exit_flag = False
        pixels.fill((0, 0, 0))
        pixels.show()
        State.enter(self, machine)

    def exit(self, machine):
        current_brightness = self.brightness
        State.exit(self, machine)

    def update(self, machine):
        pixels.fill((0, 0, 0))
        pixels.show()
        for i in range(self.bitmap.width):
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

            if self.exit_flag is True:
                machine.go_to_state("party")
                break

            # Use a rainbow of colors, shifting each column of pixels
            self.hue = self.hue + 7
            if self.hue >= 256:
                self.hue = self.hue - 256
            color = colorwheel(self.hue)

            # Scoot the old text left by 1 pixel
            pixels[7:41] = pixels[:34]

            # Draw in the next line of text
            for y in range(7):
                # Select black or color depending on the bitmap pixel
                pixels[6 - y] = color * self.bitmap[i, y]
            pixels.show()
            time.sleep(0.15)
