import os
import board
import busio
import digitalio
import neopixel
from time import sleep
import adafruit_sdcard
import pio_i2s

# Setup neopixels
pixel_pin = board.GP11
num_pixels = 42
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)

# Setup microphone
# Uncomment the following and adjust pins
'''
mic = pio_i2s.I2S(
    bit_clock=board.GP0,  # word select is GP1
    data_in=board.GP2,
    channel_count=1,
    sample_rate=48000,
    bits_per_sample=16,
    samples_signed=True,
)
'''

# Setup accelerometer


# Setup SD Card
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(board.GP5)
try:
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
except:
    sleep(1)

