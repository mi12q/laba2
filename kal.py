import spidev
import time
import RPi.GPIO as GPIO
import numpy as np
import jetFunctions as jet



jet.initSpiAdc()

samples = []
with open('70.txt','w') as file:

    for i in range(500):
        file.write(str(jet.getAdc()))
        file.write('\n')
        time.sleep(0.01)



    