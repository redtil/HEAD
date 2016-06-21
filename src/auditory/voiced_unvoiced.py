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

def unvoiced_starting_pts(f0,vSig):
    #register unvoiced signal starting points
    start = False
    cnt = 0
    for i in f0:
        if i == 0 and start == False:
            pt = cnt * 80
            vSig["unvoicedStart"].append(pt)
            start = True
        if i != 0:
            start = False
        cnt = cnt + 1

def voiced_starting_pts(f0,vSig):
    #register voiced signal starting points
    start = False
    cnt = 0
    for i in f0:
        if i != 0 and start == False:
            pt = cnt * 80
            vSig["voicedStart"].append(pt)
            start = True
        if i == 0:
            start = False
        cnt = cnt + 1

def length_voiced_region(lenSndArray, lengthVoiced,vSig):
    #length of each voiced region
    cnt = 0
    for i in vSig["voicedStart"]:
        if vSig["voicedStart"][0] != 0:
            if cnt+1 == len(vSig["unvoicedStart"]):
                lengthVoiced.append(len(lenSndArray)-i)
            else:
                lengthVoiced.append(numpy.abs(vSig["unvoicedStart"][cnt+1]-i))
        else:
            if cnt == len(vSig["unvoicedStart"]):
                lengthVoiced.append(lenSndArray-i)
            else:
                lengthVoiced.append(numpy.abs(vSig["unvoicedStart"][cnt]-i))
        cnt = cnt + 1

def length_unvoiced_region(lenSndArray,lengthUnvoiced,vSig):
    #length of each unvoiced region
    cnt = 0
    for i in vSig["unvoicedStart"]:
        if vSig["unvoicedStart"][0] == 0:
            if cnt == len(vSig["voicedStart"]):
                lengthUnvoiced.append(lenSndArray-i)
            else:
                lengthUnvoiced.append(numpy.abs(vSig["voicedStart"][cnt]-i))
        else:
            if cnt+1 == len(vSig["voicedStart"]):
                lengthUnvoiced.append(lenSndArray-i)
            else:
                lengthUnvoiced.append(numpy.abs(vSig["voicedStart"][cnt+1]-i))
        cnt  = cnt + 1

def get_voiced_region_array(sndarrayOne,vSig,lengthVoiced):
    xVoiced = []
    cnt = 0
    cntOne = 0
    for i in sndarrayOne:
        if cnt+1 != len(vSig["voicedStart"]) and cntOne == vSig["voicedStart"][cnt+1]:
            cnt = cnt + 1
        if cntOne >= vSig["voicedStart"][cnt] and cntOne <= vSig["voicedStart"][cnt]+ lengthVoiced[cnt]:
            xVoiced.append(i)
        cntOne = cntOne + 1
    return xVoiced

def get_unvoiced_region_array(sndarrayOne,vSig,lengthUnvoiced):
    xUnvoiced = []
    cnt = 0
    cntOne = 0
    for i in sndarrayOne:
        if cnt+1 != len(vSig["unvoicedStart"]) and cntOne == vSig["unvoicedStart"][cnt+1]:
            cnt = cnt + 1
        if cntOne >= vSig["unvoicedStart"][cnt] and cntOne <= vSig["unvoicedStart"][cnt]+ lengthUnvoiced[cnt]:
            xUnvoiced.append(i)
        cntOne = cntOne + 1
    return xUnvoiced

def plot_voiced_region(xVoiced):
    xVoiced = numpy.asarray(xVoiced).astype(numpy.float32)
    # hopsize = 10 # 5ms for 16kHz data
    f0 = pysptk.swipe(numpy.asarray(xVoiced).astype(numpy.float64), 44100, 80,10,600,0.3,1)
    fnew = []
    cnti = []
    cnt = 0
    for i in f0:
        if i != 0:
            cnti.append(cnt)
            fnew.append(i)
        cnt = cnt + 1
    pitch_mean = numpy.mean(fnew)
    cent = []
    for i in fnew:
        cent.append(dspUtil.hertzToCents(i, pitch_mean))

    import matplotlib.pyplot as plt
    plt.close()
    plt.plot(f0,'-o', linewidth=2, label="F0 trajectory estimated by SWIPE'")
    plt.xlim(0, len(f0))
    plt.legend()
    plt.show()

def get_signal_voiced_unvoiced_starting_info(x,fs):
    f0 = get_freq_array(x,fs)
    vSig = {"unvoicedStart":[],"voicedStart":[]}
    unvoiced_starting_pts(f0,vSig)
    voiced_starting_pts(f0,vSig)
    return vSig

def get_signal_voiced_length_info(sndarrayOne,vSig):
    lengthVoiced = []
    length_voiced_region(len(sndarrayOne),lengthVoiced,vSig)
    return lengthVoiced

def get_signal_unvoiced_length_info(sndarrayOne,vSig):
    lengthUnvoiced = []
    length_unvoiced_region(len(sndarrayOne),lengthUnvoiced,vSig)
    return lengthUnvoiced

def get_one_channel_array(sndarray):
    xOne = []
    for i in sndarray:
        xOne.append(i[1])
    return xOne

def get_freq_array(sndarray,fs):
    xOne = []
    for i in sndarray:
        xOne.append(i[1])
    f0 = pysptk.swipe(numpy.asarray(xOne).astype(numpy.float64), fs, 80,10,600,0.3,1)
    return f0

def merge_voiced_unvoiced_regions(xVoiced,xUnvoiced,vSig):
    total_len = len(xVoiced) + len(xUnvoiced)
    cnt = 0
    voicedCnt = 0
    unvoicedCnt = 0
    xMerged = []
    if vSig["voicedStart"][0] == 0:
        start = "voiced"
        switch = "voiced"
    else:
        start = "unvoiced"
        switch = "unvoiced"
    for i in range(total_len):
        if start == "unvoiced":
            if  switch == "voiced" and cnt+1 == len(vSig["unvoicedStart"]):
                # print "I am here 0 " + str(i) + " " + str(cnt) + " " + str(voicedCnt)
                xMerged.append(xVoiced[voicedCnt])
                voicedCnt = voicedCnt + 1
            elif switch == "unvoiced" and cnt == len(vSig["voicedStart"]):
                # print "I am here 1 " + str(i) + " " + str(cnt) + " " +  str(unvoicedCnt)
                xMerged.append(xUnvoiced[unvoicedCnt])
                unvoicedCnt = unvoicedCnt + 1
            elif switch == "unvoiced" and i < vSig["voicedStart"][cnt] :
                # print "I am here 2 " + str(i) + " " + str(cnt) + " " +  str(unvoicedCnt)
                xMerged.append(xUnvoiced[unvoicedCnt])
                unvoicedCnt = unvoicedCnt + 1
            elif switch == "voiced" and i < vSig["unvoicedStart"][cnt+1]:
                # print "I am here 3 " + str(i) + " " + str(cnt) + " " + str(voicedCnt)
                xMerged.append(xVoiced[voicedCnt])
                voicedCnt = voicedCnt + 1
            elif switch == "voiced":
                # print "I am here 0 " + str(i) + " " + str(cnt) + " " + str(unvoicedCnt)
                switch = "unvoiced"
                xMerged.append(xUnvoiced[unvoicedCnt])
                cnt = cnt + 1
            else:
                # print "I am here 1 " + str(i) + " " + str(cnt) + " " + str(voicedCnt)
                switch = "voiced"
                xMerged.append(xVoiced[voicedCnt])
        else:
            if cnt+1 == len(vSig["voicedStart"]):
                xMerged.append(xUnvoiced[unvoicedCnt])
                unvoicedCnt = unvoicedCnt + 1
            if cnt == len(vSig["unvoicedStart"]):
                xMerged.append(xVoiced[voicedCnt])
                voicedCnt = voicedCnt + 1
            if switch == "voiced" and i <= vSig["unvoicedStart"][cnt] :
                xMerged.append(xUnvoiced[unvoicedCnt])
                unvoicedCnt = unvoicedCnt + 1
            elif switch == "unvoiced" and i <= vSig["voicedStart"][cnt+1]:
                xMerged.append(xVoiced[voicedCnt])
                voicedCnt = voicedCnt + 1
            elif switch == "voiced":
                switch = "unvoiced"
                xMerged.append(xUnvoiced[unvoicedCnt])
                unvoicedCnt = unvoicedCnt + 1
            else:
                switch = "voiced"
                xMerged.append(xVoiced[voicedCnt])
                voicedCnt = voicedCnt + 1
                cnt += cnt
    return xMerged


def make_two_channels(sndarrayOne):
    sndarrayTwo = []
    for i in sndarrayOne:
        bz=[i,i]
        sndarrayTwo.append(bz)
    return sndarrayTwo

def write_to_new_file(filename,path,sndarray):
    sndarray = numpy.asarray(sndarray)
    file = path + filename
    scipy.io.wavfile.write(file,44100,numpy.asarray(sndarray))

if __name__ == "__main__":
    mydir = 'C:/Users/rediet/Documents/Vocie-samples/'
    myfile = 'amy.wav'
    file = os.path.join(mydir, myfile)
    fs, x = wavfile.read(file)
    xOne = get_one_channel_array(x)

    #vSig is a dictonary of voiced and unvoiced regions starting points
    vSig = get_signal_voiced_unvoiced_starting_info(x,fs)
    lengthVoiced = get_signal_voiced_length_info(xOne,vSig)
    lengthUnvoiced = get_signal_unvoiced_length_info(xOne,vSig)

    #make a signal array with only voiced regions
    xVoiced = get_voiced_region_array(xOne,vSig,lengthVoiced)
    xUnvoiced = get_unvoiced_region_array(xOne,vSig,lengthUnvoiced)
    xMerged = merge_voiced_unvoiced_regions(xVoiced,xUnvoiced,vSig)

    # plot_voiced_region(xVoiced)
    # plot_voiced_region(xMerged)
    # xTwo = make_two_channels(x)
    xMergedTwo = make_two_channels(xMerged)
    path = 'C:/Users/rediet/Documents/Vocie-samples/'
    write_to_new_file('amyMerged.wav',path,xMergedTwo)
    # scipy.io.wavfile.write('C:/Users/rediet/Documents/Vocie-samples/amyMerged.wav',fs,numpy.asarray(xMergedTwo))
