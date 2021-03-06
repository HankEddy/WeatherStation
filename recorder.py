#!/usr/bin/python

import time
from datetime import date
from datetime import datetime
import board
import busio
import adafruit_ina219
import adafruit_ltr390
from w1thermsensor import W1ThermSensor
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_pm25.i2c import PM25_I2C
import os.path
import csv

# pm25_resetpin = None
# pm25_setpin = None
# Add these later sometime to enable sleep for the Particulate Sensor

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

now = datetime.now()
voltmeter = adafruit_ina219.INA219(i2c)
lightmeter = adafruit_ltr390.LTR390(i2c)
tempsensor = W1ThermSensor()
barometer = adafruit_bme280.Adafruit_BME280_I2C(i2c)
particlesensor = PM25_I2C(i2c)
# If set/reset pins get defined later, add them here^

aqdata = particlesensor.read()
pressurekpa = barometer.pressure/10
current_time = now.strftime("%H:%M")
todayfile = now.strftime("./history/%Y-%m-%d.csv")
file_exists = os.path.exists(todayfile)
# intermediate steps go here

volts = float('%0.2f' % voltmeter.bus_voltage)
milliamps = float('%0.2f' % voltmeter.current)
lux = float('%0.2f' % lightmeter.lux)
uvindex = float('%0.2f' % lightmeter.uvi)
temperature = float('%0.2f' % tempsensor.get_temperature())
humidity = float('%0.2f' % barometer.humidity)
pressure = float('%0.2f' % pressurekpa)
particles25 = float('%0.2f' % aqdata["pm25 env"])

print ("Weather Logged @", current_time, "-", volts, "Volts")

# create/open daily history file and add the current data as a new line, delimited by commas
if not file_exists:
    with open(todayfile, 'a', newline='') as dailyLog:
        writer = csv.writer(dailyLog, delimiter=',')
        writer.writerow(["Time", " V ", " mA ", " tC ", " %rh ", " kPa ", " PM25 "])
        
with open(todayfile, 'a', newline='') as dailyLog:
    writer = csv.writer(dailyLog, delimiter=',')
    writer.writerow([current_time, volts, milliamps, temperature, humidity, pressure, particles25])

exit()
