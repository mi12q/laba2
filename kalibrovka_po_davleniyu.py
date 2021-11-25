import matplotlib.pyplot as plt
import numpy as np
import spidev
import time

maxvoltage = 3.3
values = []
preses = []
vals = []
nums = []

#Массив маркеров настроишь на основании полученных данных
#markers_on = [int(i) for i in range(0,20000,100)]

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1600000

print("Введите текущее давление в Па, если закончили, введите 1000")
pres = int(input())

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

try:
    while pres != 1000:
        srval = 0
        with open("/home/gr106/Desktop/jet-starter-kit/data/" + str(pres) + " PA.txt", "w") as f:
            f.write('- Jet Lab\n')
            f.write('- Date: {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            f.write('- Step: {} motor steps\n'.format(10))
        for i in range(550):
            value = getAdc()
            srval += value
            with open("/home/gr106/Desktop/jet-starter-kit/data/" + str(pres) + " PA.txt", "a") as f:
                f.write(str(value) + '\n')
        srval = srval / 550
        preses.append(pres)
        values.append(srval)
        print("Введите текущее давление в Па, если закончили, введите 1000")
        pres = int(input())
    values = np.array(values)
    preses = np.array(preses)
    (k, b) = np.polyfit(values, preses, 1)
    vals = []
    nums = []
    k = (preses[-1] - preses[0]) / (values[-1] - values[0])
    b = values[0]
    for i in range(0, 1400, 100):
        vals.append(b + k*i)
        nums.append(i)
    
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.plot(values, preses,
            linestyle='--',
            linewidth=3,
            color='darkmagenta')
    ax.plot(nums, vals,
            linestyle='-',
            linewidth=1,
            color='red'
            )
    ax.set_title('Калибровка Давления', style='italic')
    ax.legend(labels=("значения в точках", "аппроксимирующая"), loc="upper right")
    ax.set_xlabel('значения давления в у е')
    ax.set_ylabel('давление (Па)')
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
    plt.savefig('/home/gr106/Desktop/jet-starter-kit/plots/pressure-calibration.png')
finally:
    plt.show()
    spi.close()





