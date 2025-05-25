import time
#from setup import rotary_enc


class State(object):
    def __init__(self):
        pass

    @property
    def name(self):
        return ""

    def enter(self, core_machine):
        time.sleep(0.3)
        pass

    def exit(self, core_machine):
        pass

    def update(self, core_machine):
        return True


class StateMachine(object):
    def __init__(self):
        self.state = None
        self.states = {}
        #self.last_enc1_pos = rotary_enc.value()
        #self.paused_state = None
        self.ticks_ms = 0
        #self.animation = None

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            self.state.exit(self)
        self.state = self.states[state_name]
        self.state.enter(self)

    def update(self):
        if self.state:
            self.state.update(self)
            if self.ticks_ms > 0:
                time.sleep(self.ticks_ms / 1000)

    # When pausing, don't exit the state
    def pause(self):
        self.state = self.states["paused"]
        self.state.enter(self)

    # When resuming, don't re-enter the state
    def resume_state(self, state_name):
        if self.state:
            self.state.exit(self)
        self.state = self.states[state_name]