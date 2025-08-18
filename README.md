```
 ______                   ____            _            
|__  (_)_ __  _ __  _   _| __ )  __ _  __| | __ _  ___ 
  / /| | '_ \| '_ \| | | |  _ \ / _` |/ _` |/ _` |/ _ \
 / /_| | |_) | |_) | |_| | |_) | (_| | (_| | (_| |  __/
/____|_| .__/| .__/ \__, |____/ \__,_|\__,_|\__, |\___|
       |_|   |_|    |___/                   |___/      
```

DCZia Presents: The 2025 Zippy Badge

It blinks, it bloops*, it does stuff.

**Hardware**
* PiPico 2040 MCU
* Between 1 and 42 NeoPixel LEDs
* Microphone, accelerometer, and a SD card slot (not implemented, but go wild if you want)
* Powered by USB C or AA batteries.


\* Blooping not avaliable in all areas, not valid in NJ, void where prohibited, if you experience a rash or itching ask your doctor if blooping is right for you.

**User Manual**

As of Defcon, the UI is as follows - there is a four direction joystick on the right side of the badge. Clicking it in, will chnage modes, up and down will change brightness, and left and right do nothing for now. The first mode is the rainbow mode, mode 2 is accelerometer reactive and tilting the badge left, right, forward or back, will change the color. Mode 3 is a sound reactive party mode, and we tried to make an auto senseing volume / gain adjustment, but we will see if it works for parties, or if its just pegged. Power switch is on the bottom if you are using batteries, and the DFU programming buttion is well recessed (sorry) next to it. 

**Assembly / Disassembly**

The badge comes fully assembled. You can power it with a usb-c cable and a power supply of your choosing. You can also solder on the included AA battery pack. On the back of the board there are two pads, marked + and - Solder the red wire from the battery holder to the + and the black wire to the - 

Head to the HHV if you need help soldering. The case screws on with four screws. They are M2x4, self tapping or machine. You can download our shell design and print your own if you wish. Let us know if you make something cool!

**Programming / Updating**

The badge is powered by a Raspberry Pi 2040 MCU. You can find official docs for progamming here https://www.raspberrypi.com/products/rp2040/

The TL;DR is - copy our repo, plug the badge into your computer and you should see a drive appear (or not if you rolled your own linux distro that has no automounter, but you probably know what to do here already, if thats you) called "Circuitpython" Drag the files inside our repo's software directory to that drive (the .py files, and library folders). After the files are copied the badge should reboot with the new code. Sometimes the badge can reboot early and get in a weird state. You can delete everything on the drive and try again. If the badge is in a really weird state, you can hold down the bootloader button while the badge is unplugged, plug it in, and you should see a different named drive appear. Here you can drop our U2F firmwre blob which has circuitpython and our code in one file to update the badge. Hit us up on Discord / BSky if you have questions, or drop an issue here.

