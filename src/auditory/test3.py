import matplotlib.pyplot as plt
import numpy
from swipe import swipe

import dspUtil

pitch = swipe('/home/zelalem/Documents/Vocie-samples/amy.wav', 75, 600) # read in pitch track via swipe
data ={}
time=[]
frequency=[]
cent =[]

for (t, pitch) in pitch:
    if pitch < 600:  # hz
        print t, '*****************', pitch
        time.append(t)
        frequency.append(pitch)

data['Time'] = time
data['Frequency'] = frequency

pitch_mean= numpy.mean(pitch)
print pitch_mean
for i in frequency:
    cent.append(dspUtil.hertzToCents(i,baseFreq=pitch_mean))
print cent


plt.figure(1)
plt.xlabel('Time (s)')
plt.ylabel('pitch (cent)')
plt.plot(data['Time'], cent)
plt.gcf().autofmt_xdate()
plt.title('Cent vs Time')
plt.show()

