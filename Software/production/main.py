from state import StateMachine
from state_startup import StartupState

# from state_menu import MenuState
from state_party import PartyState
from state_rave import RaveState
from state_accel import AccelState
from state_scroll import ScrollState

current_brightness = 0.1


core_machine = StateMachine()
core_machine.add_state(StartupState())
core_machine.add_state(PartyState())
core_machine.add_state(AccelState())
core_machine.add_state(RaveState())
core_machine.add_state(ScrollState())

core_machine.go_to_state("startup")

while True:
    core_machine.update()
