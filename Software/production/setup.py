import board
import busio
import storage
import digitalio
import neopixel
from time import sleep
import adafruit_sdcard
import pio_i2s
import adafruit_msa3xx
import keypad

# Setup neopixels
pixel_pin = board.GP13
num_pixels = 42
current_brightness = 0.1
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=current_brightness, auto_write=False
)

# Setup microphone
# Uncomment the following
mic = pio_i2s.I2S(
    bit_clock=board.GP0,  # word select is GP1
    data_in=board.GP3,
    channel_count=2,
    sample_rate=16000,
    bits_per_sample=16,
    samples_signed=True,
    buffer_size=4,
)

# Setup accelerometer
# SDA = 16
# SCL = 17
i2c = busio.I2C(board.GP17, board.GP16)
sensor = adafruit_msa3xx.MSA301(i2c)

# Setup d-pad
key_pins = (
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
)

keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)


# Setup SD Card
spi = busio.SPI(board.GP6, board.GP7, board.GP4)
cs = digitalio.DigitalInOut(board.GP5)
try:
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
except:
    # add some feedback if it doesn't mount
    pixels.brightness = 0.05
    pixels.fill((255, 0, 0))
    pixels.show()
    sleep(0.2)
    pixels.fill((0, 255, 0))
    pixels.show()
    sleep(0.2)
    pixels.fill((0, 0, 255))
    pixels.show()
    sleep(0.2)
    pixels.fill((0, 0, 0))
