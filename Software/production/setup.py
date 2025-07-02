import os
import board
import busio
import digitalio
import neopixel
from time import sleep
import adafruit_sdcard
import pio_i2s
import adafruit_msa3xx
from digitalio import DigitalInOut, Direction, Pull

# Setup neopixels
pixel_pin = board.GP13
num_pixels = 42
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)

# Setup microphone
# Uncomment the following
mic = pio_i2s.I2S(
    bit_clock=board.GP0,  # word select is GP1
    data_in=board.GP2,
    channel_count=1,
    sample_rate=48000,
    bits_per_sample=16,
    samples_signed=True,
)

# Setup accelerometer
# SDA = 16
# SCL = 17
i2c = board.I2C()
msa = adafruit_msa3xx.MSA301(i2c)

# Setup d-pad
# Pins may be wrong, wasn't clear on schematic
dpad_up = DigitalInOut(board.GP8)
dpad_up.direction = Direction.INPUT
dpad_up.pull = Pull.UP

dpad_down = DigitalInOut(board.GP9)
dpad_down.direction = Direction.INPUT
dpad_down.pull = Pull.UP

dpad_left = DigitalInOut(board.GP10)
dpad_left.direction = Direction.INPUT
dpad_left.pull = Pull.UP

dpad_right = DigitalInOut(board.GP11)
dpad_right.direction = Direction.INPUT
dpad_right.pull = Pull.UP

dpad_button = DigitalInOut(board.GP12)
dpad_button.direction = Direction.INPUT
dpad_button.pull = Pull.UP


# Setup SD Card
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(board.GP5)
try:
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
except:
    sleep(1)
