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
import heapq

def get_freq_regions_from_voiced_region(voiced_region_range, chunk_size):
    freq_regions = []
    rng = (voiced_region_range[1] - voiced_region_range[0] + 1)/chunk_size
    for i in range(0,rng):
        start = i * chunk_size
        end = start + chunk_size - 1
        freq_region = []
        freq_region.append(start)
        freq_region.append(end)
        freq_regions.append(freq_region)
    return freq_regions

def get_freq_chunk(sndarray,chunk_start,chunk_size):
    f0 = voi.get_freq_array(sndarray,44100)
    spot = chunk_start/chunk_size
    return f0[spot]

def get_pitch_marks_voiced_chunk(sndarray,freq,chunk_start,chunk_size, numPitchMarks):
    chunk_end = chunk_start + chunk_size - 1
    pitch_marks = []
    factor = 0.7
    fctr = 1 - factor
    tm = numpy.argmax(sndarray)
    window_start = tm + fctr*freq
    if window_start <= chunk_start:
        window_start = chunk_start
    window_end = tm - fctr*freq
    while window_start <= chunk_end:
        if window_end >= chunk_end:
            window_end == chunk_end
        pitch_marks.append(tm)
        derivative = numpy.gradient(sndarray[window_start:window_end])
        ind = numpy.where(derivative == 0)[0]
        vals = []
        for i in ind:
            vals.append(sndarray(i))
        pitchMarksInd = numPitchMarks
        while pitchMarksInd > 1:
            res = heapq.nlargest(i, vals)
            indVals = numpy.where(vals == res)[0]
            spot_chunk = ind[indVals]
            pitch_marks.append(chunk_start + spot_chunk)
            pitchMarksInd = pitchMarksInd - 1
        window_start = tm + factor*freq
        window_end = tm + (2-factor) * freq
        tm = numpy.argmax(sndarray[window_start:window_end])
    return pitch_marks

def get_pitch_marks_voiced_region(sndarray, voiced_region, chunk_size):
    pitch_marks = []
    len = voiced_region[1] - voiced_region[0] + 1
    steps = len/chunk_size
    for i in steps:
        chunk_start = i * chunk_size
        freq = get_freq_chunk(sndarray,chunk_start,chunk_size)
        pitch_marks_chunk = get_pitch_marks_voiced_chunk(sndarray,freq,chunk_start, chunk_size)
        for i in pitch_marks_chunk:
            pitch_marks.append(i)
    return pitch_marks

def get_pitch_marks_voiced_regions(sndarray,voiced_regions, chunk_size):
    pitch_marks = []
    for i in voiced_regions:
        pitch_marks_region = get_pitch_marks_voiced_region(sndarray, i, chunk_size)
        for j in pitch_marks_region:
            pitch_marks.append(j)
    return pitch_marks

def get_pitch_marks_unvoiced_regions(sndarray,unvoiced_regions):
    return

def get_pitch_marks(sndarray,chunk_size):
    return

if __name__ == "__main__":

    filename= "C:/Users/rediet/Documents/Vocie-samples/kendra.wav"
    filename500= "C:/Users/rediet/Documents/Vocie-samples/kendra500.wav"
    filenameFM = "C:/Users/rediet/Documents/Vocie-samples/kendraFM.wav"
    filenameVoiced = "C:/Users/rediet/Documents/Vocie-samples/kendraVoiced.wav"
    filenameVibrato = "C:/Users/rediet/Documents/Vocie-samples/kendraVibrato.wav"

    fs, x = wavfile.read(filename)
    y = numpy.arange(0,len(x),1)
    x = voi.get_one_channel_array(x)
    # x = x[95000:96000]
    # y = y[0:1000]
    voi.plot(y,x,len(x),"signal amplitude")
    #
    # f0 = voi.get_freq_array(x, 44100)
    # x = numpy.arange(0,len(f0),1)
    # voi.plot(x,f0, len(f0), "frequency spectrum")
    # freq_regions = get_freq_regions_from_voiced_region([0,999],20)
    # print freq_regions

