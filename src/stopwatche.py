import time as tm
import datetime
import logging

################
# Stopwatch use:
# reset->start->stop->reset->
################

class IncorrectStateChange(Exception):
    pass

class StopwatchStateEnum:
    STATE_BASE = "Base state"
    NOT_STARTED = "Measure not started yet"
    STARTED = "Measure started"
    FINISHED = "Measure ready to handle"

class Stopwatch:
    def __init__(self):
        self.machine = StopwatchStateInitialized(self)
    def start(self):
        self.machine.start()
    def stop(self):
        self.machine.stop()
    def reset(self):
        self.machine.reset()
    def hadleResult(self):
        if self.machine.stat == StopwatchStateEnum.FINISHED:
            result = self.tmStop - self.tmStart
            self.machine.reset()
            return result
        else:
            logging.warning(f"Cannot handle, Machine current state is {self.machine.stat}")

class StopwatchStateBase(object):
    def __init__(self):
        self.stat = StopwatchStateEnum.STATE_BASE
    def start(self):
        raise Exception("")
    def stop(self):
        raise Exception("")
    def reset(self):
        self.instance.tmStart = self.instance.tmStop = tm.clock()
        self.instance.machine = StopwatchStateInitialized(self.instance)
##########################################################
class StopwatchStateInitialized(StopwatchStateBase):
    def __init__(self, device):
        super(StopwatchStateInitialized, self).__init__()
        self.instance = device
        self.stat = StopwatchStateEnum.NOT_STARTED
    def start(self):
        self.instance.tmStart = tm.clock()
        self.instance.machine = StopwatchStateStarted(self.instance)
    def stop(self):
        raise IncorrectStateChange()
##########################################################
class StopwatchStateStarted(StopwatchStateBase):
    def __init__(self, device):
        super(StopwatchStateStarted, self).__init__()
        self.instance = device
        self.stat = StopwatchStateEnum.STARTED
    def start(self):
        raise Exception("Stopwatch already started")
    def stop(self):
        self.instance.tmStop = tm.clock()
        self.instance.machine = StopwatchStateFinished(self.instance)
##########################################################
class StopwatchStateFinished(StopwatchStateBase):
    def __init__(self, device):
        super(StopwatchStateFinished, self).__init__()
        self.instance = device
        self.stat = StopwatchStateEnum.FINISHED
    def start(self):
        raise Exception("Stopwatch finished work, reset to take next measure")
    def stop(self):
        pass
##########################################################