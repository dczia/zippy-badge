#import os
#import time
#import board
#import neopixel
#from rainbowio import colorwheel


from state import State, StateMachine
from state_startup import StartupState
#from state_menu import MenuState
from state_party import PartyState
from state_rave import RaveState


core_machine = StateMachine()
core_machine.add_state(StartupState())
#core_machine.add_state(MenuState())
core_machine.add_state(PartyState())
core_machine.add_state(RaveState())

core_machine.go_to_state("startup")

while True:
    core_machine.update()
