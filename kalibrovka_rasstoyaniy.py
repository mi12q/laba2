import matplotlib.pyplot as plt
import numpy as np
import spidev
import time

maxvoltage = 3.3
values = []
shags = []
vals = []
nums = []

#Массив маркеров настроишь на основании полученных данных
#markers_on = [int(i) for i in range(0,20000,100)]

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1600000

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

try:
    with open("/home/gr106/Desktop/jet-starter-kit/data/shagi.txt", "r") as f:
        for line in f.readlines():
            (shag, val) = (line.split())
            values.append(float(val))
            shags.append(float(shag))
    values = np.array(values)
    shags = np.array(shags)
    (k, b) = np.polyfit(values, shags, 1)
    vals = []
    nums = []
    for i in range(0, 80, 2):
        vals.append(b + k*i)
        nums.append(i)
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.plot(values, shags,
            linestyle='--',
            linewidth=3,
            color='darkmagenta')
    ax.plot(nums, vals,
            linestyle='-',
            linewidth=1,
            color='red'
            )
    ax.set_title('Задание каллибровки по расстоянию', style='italic')
    ax.legend(labels=("значения в точках", "аппроксимирующая"), loc="upper right")
    ax.set_ylabel('значения длины в шагах')
    ax.set_xlabel('длина (мм)')
    ax.axes.grid(
        which="major",
        linewidth="0.4",
    )
    ax.minorticks_on()
    ax.axes.grid(
       which = "minor",
       linewidth = "0.2"
    )
    print('угловой коэффициент = ' + str(k))
    print('Свободный член = ' + str(b))
    plt.savefig('/home/gr106/Desktop/jet-starter-kit/plots/distance-calibration.png')
finally:
    plt.show()
    spi.close()





