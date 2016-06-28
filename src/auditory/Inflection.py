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
import voiced_unvoiced as voi
import time
import pygame
import pitch_shifter

s = Server(audio='pa', nchnls=2).boot()
s.start()
# mydir = 'C:/Users/rediet/Documents/Vocie-samples/'
# myfile = 'amy.wav'
# file = os.path.join(mydir, myfile)
# fs, x = wavfile.read(file)
#
#
# xOne = voi.get_one_channel_array(x)
# vSig = voi.get_signal_voiced_unvoiced_starting_info(x,fs)
# lengthVoiced = voi.get_signal_voiced_length_info(xOne,vSig)
# lengthUnvoiced = voi.get_signal_unvoiced_length_info(xOne,vSig)
#
# #make a signal array with only voiced regions
# xVoiced = voi.get_voiced_region_array(xOne,vSig,lengthVoiced)
#
# xVoiced500 = []
# samps = secToSamps(0.5)
# cnt = 0
# for i in xVoiced:
#     if cnt < samps:
#         xVoiced500.append(i)
#     cnt = cnt + 1
# # voi.plot_voiced_region(xVoiced500)
# xVoiced500Two = voi.make_two_channels(xVoiced500)
# voi.write_to_new_file('amy500.wav',mydir,xVoiced500Two)

# mydir = 'C:/Users/rediet/Documents/Vocie-samples/'
# myfile = 'amy.wav'
# file = os.path.join(mydir, myfile)
# fs, x = wavfile.read(file)
# f0 = voi.get_freq_array(x,fs)
# xOne = voi.get_one_channel_array(x)
# voi.write_to_new_file('amyPitchShifted.wav',mydir,pitch_shifter.pitchshift(xOne,2.0))

# fnew = []
# cnti = []
# cnt = 0
# for i in f0:
#     if i != 0:
#         cnti.append(cnt)
#         fnew.append(i)
#     cnt = cnt + 1
# pitch_mean = numpy.mean(fnew)
# cnti4 = numpy.asarray(cnti)/4.0
# newSinArr = (numpy.sin(cnti4))*dspUtil.centsToHertz(200, pitch_mean)
# diffarr = []
# for i in numpy.arange(0,len(cnti4),1):
#     diffarr.append(newSinArr[i]-fnew[i])
#
#
# # voi.write_to_new_file('jaggedSineWave1.wav',mydir,diffarr)
# plt.plot(cnti,newSinArr,'-o', cnti, fnew,'-bo',cnti, diffarr,'-ro', linewidth=2, label="F0 trajectory estimated by SWIPE'")
# plt.xlim(0, len(f0))
# plt.legend()
# plt.show()
#
#
file= "C:/Users/rediet/Documents/Vocie-samples/kendra.wav"
# filetwo = "C:/Users/rediet/Documents/Vocie-samples/kendraVibrato.wav"
fileRec = "C:/Users/rediet/Documents/Vocie-samples/kendraVibrato.wav"
filedur = sndinfo(file)[1]

sf = SfPlayer(file, speed=1, loop=False)
# sf2 = SfPlayer(filetwo,speed=1,loop=False)
lf2 = Sine(freq=2.5, mul= 50,add=1)
# # lf2 = 185.27436
# # lf2 = 0
s.recstart(filename=fileRec)
b = FreqShift(sf, shift=lf2, mul=1).out()
time.sleep(filedur)
s.recstop()



# scipy.io.wavfile.write('C:/Users/rediet/Documents/Vocie-samples/xenencounter_23sin.wav',fs,numpy.asarray(yfile))

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




