import MTECH_GPIO as GPIO
import numpy as numpy
import matplotlib.pyplot as plt
from collections import deque
import time
from HC_SR04 import HC_SR04
from Unit import Unit
from FilteredDistanceSensor import FilteredDistanceSensor

repeat = True

trig = 20
echo = 21

pingTime = 0

GPIO.setmode(GPIO.BCM)

sensor = HC_SR04(echo, trig)
filterSensor = FilteredDistanceSensor(sensor, 'raw', Unit.METER)


# How many measurements to display at once
WINDOW_SIZE = 100

distances = deque(maxlen=WINDOW_SIZE)
times = deque(maxlen=WINDOW_SIZE)

plt.ion()  # Interactive mode
fig, ax = plt.subplots()

line, = ax.plot([], [], 'b-')

ax.set_xlabel("Time (s)")
ax.set_ylabel("Distance (cm)")
ax.set_title("HC-SR04 Distance")
ax.grid(True)

start_time = time.time()

try:
    while True:
        dist = filterSensor.getFilteredDistance()

        current_time = time.time() - start_time
        times.append(current_time)
        distances.append(dist)

        line.set_data(times, distances)

        # Make the axes follow the incoming data
        ax.relim()
        ax.autoscale_view()

        # Redraw
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Sensor sampling rate
        time.sleep(0.05)
except KeyboardInterrupt:
    pass 
