import sys
sys.path.append("..")
from utils import Stopwatch
import matplotlib.pyplot as plt

stopwatch1 = Stopwatch.Stopwatch()
measurements = list()

outsaiders = 0
retries=1000000
for i in range(retries):
    stopwatch1.reset()
    stopwatch1.start()
    stopwatch1.stop()
    res = stopwatch1.hadleResult()
    measurements.append(res)
    print("% 2.20f"% res)
    if res > 1.0e-03:
        outsaiders = outsaiders + 1

suma = 0
for measure in measurements:
    suma = suma + pow(measure,2)
suma = suma/len(measurements)

mse = pow(suma, 0.5)
print(f"min:{min(measurements)} max:{max(measurements)} avr:{sum(measurements)/len(measurements)} mse:{mse}")
print("{prc}%".format(prc=outsaiders/retries*100))


