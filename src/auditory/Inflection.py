from pyo import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import pysptk
import numpy
from libs import dspUtil
import scipy
import array
import voiced_unvoiced

s = Server(audio='pa', nchnls=2).boot()
s.start()
mydir = 'C:/Users/rediet/Documents/Vocie-samples/'
myfile = 'amy.wav'
file = os.path.join(mydir, myfile)
fs, x = wavfile.read(file)

vSig = voiced_unvoiced.get_signal_voiced_unvoiced_starting_info(x,fs)


















##########################################################################################
# yfile = []
# yin = []
# print secToSamps(6)
# b = numpy.arange(0,secToSamps(3),1)
# print b
# cnt = 0
# for i in x:
#     if cnt == secToSamps(2):
#         break
#     # if (i[0] > 30) or (i[0] < -30):
#     for j in i:
#         yin.append(j)
#     yfile.append(yin)
#     yin = []
#     cnt = cnt + 1
#
# yfilenew = []
# for i in yfile:
#     yfilenew.append(i[1])
#
# scipy.io.wavfile.write('C:/Users/rediet/Documents/Vocie-samples/xenencounter.wav',fs,numpy.asarray(yfile))
#
# yfilenew = numpy.asarray(yfilenew).astype(numpy.float32)
# # hopsize = 10 # 5ms for 16kHz data
# f0 = pysptk.swipe(yfilenew.astype(numpy.float64), fs, 80,10,600,0.3,1)
#
# fnew = []
# cnti = []
# cnt = 0
# for i in f0:
#     if i != 0:
#         cnti.append(cnt)
#         fnew.append(i)
#     cnt = cnt + 1
# pitch_mean = numpy.mean(fnew)
# cent = []
# for i in fnew:
#     cent.append(dspUtil.hertzToCents(i, pitch_mean))
#
# import matplotlib.pyplot as plt
# plt.close()
# plt.plot(cnti, cent,'-o', linewidth=2, label="F0 trajectory estimated by SWIPE'")
# plt.xlim(0, len(f0))
# plt.legend()
# plt.show()
#############################################################################################

############################################################################################
#sine wave
# fs = 44100
# t = numpy.arange(0, .004, 1.0/fs)
# f0 = 1000
# phi = numpy.pi/2
# A = .8
# x = A * numpy.sin(2 * numpy.pi * f0 * t + phi)
#
# plt.plot(t, x)
# plt.axis([0, .004, -.8, .8])
# plt.xlabel('time')
# plt.ylabel('amplitude')
# plt.show()
############################################################################################


# yfilenew = []
# for i in yfile:
#     yfilenew.append(i[1])
# ynew = []
# for i in yfilenew:
#     ynew.append([i,i])
# mydir = 'C:/Users/rediet/Documents/Vocie-samples/'
# myfile = 'amy.wav'
# file = os.path.join(mydir, myfile)
# fs, x = wavfile.read(file)
#
# print len(x)
# print fs
# s = Server(audio='pa', nchnls=2).boot()
# s.start()
# file= "C:/Users/rediet/Documents/Vocie-samples/amy.wav"
# sf = SfPlayer(file, speed=1, loop=False)
# sndinfo(file)
# smps = []
# for n in range(0, secToSamps(7)):

# savefile(yfile,"C:/Users/rediet/Documents/Vocie-samples/amyInflection.wav",channels=2,fileformat=0,sampletype=2)
# print smps
# lf1 = Sine(freq=.04, mul=10)
# lf1= 508.355
# lf2 = Sine(freq=200, mul= 5,add=1)
# a = SineLoop(freq=300, feedback=.1, mul=.3)
# lf1 = Sine(freq=.04, mul=30)
# lf2 = Sine(freq=.05, mul=10)
# b = FreqShift(a, shift=lf1, mul=.5).out()
# c = FreqShift(a, shift=lf2, mul=.5).out(1)
# lf2 = 185.27436
# b = FreqShift(sf, shift=lf1 , mul=2).play()

# s.gui()
# s.closeGui()




