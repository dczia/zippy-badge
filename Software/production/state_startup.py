import time

from setup import pixels
from setup import keys
from state import State

import fontio
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel
from setup import current_brightness

# from menu import menu_select, show_menu, show_select


class StartupState(State):

    @property
    def name(self):
        return "startup"

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
        self.label.text = "     DCZIA     "
        self.bitmap = self.label.bitmap
        self.brightness = current_brightness

        State.enter(self, machine)

    def exit(self, machine):
        current_brightness = self.brightness
        State.exit(self, machine)

    def update(self, machine):

        for i in range(self.bitmap.width):
            # Poll for key press and cycle to next mode, put in loop to allow intro skip
            event = keys.events.get()
            if event:
                if event.pressed:
                    if event.key_number == 1:
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
                # pixels[35+y] = color * self.bitmap[i,y]
                pixels[6 - y] = color * self.bitmap[i, y]
            pixels.show()
            time.sleep(0.15)
        machine.go_to_state("party")
