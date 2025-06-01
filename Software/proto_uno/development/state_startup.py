import time

from rainbowio import colorwheel

from setup import pixels, num_pixels
from state import State


from random import randint
#import board
#import neopixel
import fontio
from adafruit_display_text.bitmap_label import Label
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from rainbowio import colorwheel
#from menu import menu_select, show_menu, show_select


class StartupState(State):

    @property
    def name(self):
        return "startup"

    def __init__(self):
        
        # Everything in this startup should probably go somewhere more general
        # Putting it here for now to make this work quickly
        tom_thumb = bitmap_font.load_font("tom-thumb.pcf", Bitmap)

        _glyph_keys = ['bitmap', 'tile_index', 'width', 'height', 'dx', 'dy', 'shift_x', 'shift_y']
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

        self.font = PatchedFont(tom_thumb,
                           {32: {'shift_x': 1, 'dx': 0},
                            105: {'dx': 0, 'shift_x': 2},
                            33: {'dx': 0, 'shift_x': 2},
                            })


        # Create a label object
        self.label = Label(text="text", font=self.font)
        self.bitmap = self.label.bitmap

    def enter(self, machine):
        # Show party mode text
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        hue = 0
        self.label.text = "     DCZIA     "
        bitmap = self.label.bitmap
        for i in range(bitmap.width):
            # Use a rainbow of colors, shifting each column of pixels
            hue = hue + 7
            if hue >= 256:
                hue = hue - 256
            color = colorwheel(hue)
            # Scoot the old text left by 1 pixel
            pixels[:35] = pixels[7:]
            # Draw in the next line of text
            for y in range(7):
                # Select black or color depending on the bitmap pixel
                pixels[35+y] = color * bitmap[i,y]
            pixels.show()
            time.sleep(.15)
        machine.go_to_state("rave")

