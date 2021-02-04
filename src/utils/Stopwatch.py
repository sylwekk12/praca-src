import time as tm
import datetime
import logging


################
# Stopwatch use:
# reset->start->stop->reset
################
#stopwatch precision +/- 0,001
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
        self.measurements = list()

    def start(self):
        self.machine.start()

    def stop(self):
        self.machine.stop()

    def reset(self):
        self.machine.reset()

    def hadleResult(self):
        if self.machine.stat == StopwatchStateEnum.FINISHED:
            result = self.tmStop - self.tmStart
            self.measurements.append(result)
            return result
        else:
            logging.warning(f"Cannot handle, Machine current state is {self.machine.stat}")

    def getAverageMeasurement(self):
        measurementsNumber = len(self.measurements)
        return sum(self.measurements)/measurementsNumber

    def getMeasurementsList(self):
        return self.measurements

class StopwatchStateBase(object):
    def __init__(self):
        self.stat = StopwatchStateEnum.STATE_BASE
        self.instance = None

    def start(self):
        raise Exception("")

    def stop(self):
        raise Exception("")

    def reset(self):
        if self.stat is not StopwatchStateEnum.STATE_BASE:
            self._reset()
            self.instance.machine = StopwatchStateInitialized(self.instance)
        else:
            raise Exception("base ")

    def _reset(self):
        self.tmStart = self.instance.tmStop = tm.perf_counter()


##########################################################
class StopwatchStateInitialized(StopwatchStateBase):
    def __init__(self, device):
        super(StopwatchStateInitialized, self).__init__()
        self.instance = device
        self.stat = StopwatchStateEnum.NOT_STARTED

    def start(self):
        self.instance.tmStart = tm.perf_counter()
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
        self.instance.tmStop = tm.perf_counter()
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
