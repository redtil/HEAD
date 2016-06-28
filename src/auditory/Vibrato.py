import wave, struct, math
import array
import voiced_unvoiced as voi
import os
from scipy.io import wavfile
import numpy
import pysptk
from libs import dspUtil
import freqModulation as fm
from pyo import *
import pitch_shifter as ps
import matplotlib as plt

s = Server(audio='pa', nchnls=2).boot()
s.start()

filename= "C:/Users/rediet/Documents/Vocie-samples/kendra.wav"
filename500= "C:/Users/rediet/Documents/Vocie-samples/kendra500.wav"
filenameFM = "C:/Users/rediet/Documents/Vocie-samples/kendraFM.wav"
filenameVoiced = "C:/Users/rediet/Documents/Vocie-samples/kendraVoiced.wav"
filenameVibrato = "C:/Users/rediet/Documents/Vocie-samples/kendraVibrato.wav"
# xOne = voi.get_one_channel_array(x)
#
# #vSig is a dictonary of voiced and unvoiced regions starting points
# vSig = voi.get_signal_voiced_unvoiced_starting_info(x,fs)
# lengthVoiced = voi.get_signal_voiced_length_info(xOne,vSig)
# lengthUnvoiced = voi.get_signal_unvoiced_length_info(xOne,vSig)
#
# #make a signal array with only voiced regions
# xVoiced = voi.get_voiced_region_array(xOne,vSig,lengthVoiced)
# voi.write_to_new_file(filenameVoiced,xVoiced)



# fs, xVoiced= wavfile.read(filenameVoiced)
# xVoiced500 = []
# samps = secToSamps(0.5)
# cnt = 0
# xVoicedOne = voi.get_one_channel_array(xVoiced)
# for i in xVoicedOne:
#     if cnt < samps:
#         xVoiced500.append(i)
#     cnt = cnt + 1
# # voi.plot_voiced_region(xVoiced500)
# xVoiced500Two = voi.make_two_channels(xVoiced500)
# voi.write_to_new_file(filename500,xVoiced500Two)

#
fs, x = wavfile.read(filename500)
xOne = voi.get_one_channel_array(x)
cntTimeArray = numpy.arange(0,len(xOne),1)
# voi.plot(cntTimeArray,xOne,len(xOne), "amplitude")

f0 = voi.get_freq_array(xOne,fs)
cntTimeArray = numpy.arange(0,len(f0),1)
f0FMarray = fm.FreqModArray(f0,cntTimeArray,1.5,filenameFM)
# voi.plot(cntTimeArray,f0FMarray,len(voi.get_freq_array(xOne,fs)),"Modulated sine wave")


#pitch_shift
toShiftArray = []
for i in range(0,len(f0FMarray)):
    toShiftArray.append(f0FMarray[i]-f0[i])
# voi.plot(cntTimeArray,toShiftArray,len(f0), "to be shifted frequency values")

hertzToFactor = []
cnt = 0
for i in toShiftArray:
    if(numpy.float32(f0[cnt]) == 0):
        factor = 0
    else:
        factor = 1 + i/numpy.float32(f0[cnt])
    #doubling frequency in equal to increase in 12 semitones
    hertzToFactor.append(factor*6.0)
    cnt = cnt + 1
# voi.plot(cntTimeArray,hertzToFactor,len(f0), "pitch shift factor in semitones")

chunk_size = 80
xVibrato = []
for i in range(0,len(hertzToFactor)):
    if(hertzToFactor[i] == 0):
        for i in xOne[i*chunk_size:(i*chunk_size) + chunk_size-1]:
            xVibrato.append(i)
    else:
        print i
        xShifted = ps.pitchshift(xOne[i*chunk_size:i*chunk_size + chunk_size-1],hertzToFactor[i],window_size=2**5,h=2**3)
        print xShifted
        for i in xShifted:
            xVibrato.append(i)
# xVibratoTwo = voi.make_two_channels(xVibrato)
# voi.write_to_new_file(filenameVibrato,xVibrato)