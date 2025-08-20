from setup import pixels
from setup import keys
from state import State

import fontio
import time
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel
import global_tools


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
        self.label.selector = 0
        pixels.fill((0, 0, 0))
        pixels.show()
        State.enter(self, machine)

    def exit(self, machine):
        pixels.fill((0, 0, 0))
        pixels.show()
        State.exit(self, machine)

    def update(self, machine):
        self.label.yelling = ["     DCZIA     ",
                              "     ZIPPY     ",
                              "     1337  wAr3z     ",
                              "     MALORT  PLZ     ",
                              "     HACK  THE  PLANET     "]
        self.label.text = self.label.yelling[self.label.selector]
        self.bitmap = self.label.bitmap

        pixels.fill((0, 0, 0))
        pixels.show()
        for i in range(self.bitmap.width):
            event = keys.events.get()
            if event:
                if event.pressed:
                    if event.key_number == 1:
                        machine.go_to_state("rave")
                        return
                # text selection
                elif event.key_number == 2:
                    # right key
                    if self.label.selector < len(self.label.yelling) - 1:
                        self.label.selector += 1
                    else:
                        self.label.selector = 0
                    self.bitmap = self.label.bitmap
                    break
                elif event.key_number == 3:
                    # left key
                    if self.label.selector == 0:
                        self.label.selector = len(self.label.yelling) - 1
                    else:
                        self.label.selector -= 1
                    break

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

            # Use a rainbow of colors, shifting each column of pixels
            self.hue = self.hue + 7
            if self.hue >= 256:
                self.hue = self.hue - 256
            color = colorwheel(self.hue)
            if self.label.selector == len(self.label.yelling) - 2:
                # Use a fixed color for the malort text
                color = colorwheel(42)
            if self.label.selector == len(self.label.yelling) - 1:
                # Use a fixed color for the last text
                color = colorwheel(87)

            # Scoot the old text left by 1 pixel
            pixels[7:41] = pixels[:34]

            # Draw in the next line of text
            for y in range(7):
                # Select black or color depending on the bitmap pixel
                pixels[6 - y] = color * self.bitmap[i, y]
            pixels.show()
            time.sleep(0.11)
