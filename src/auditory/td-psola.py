import voiced_unvoiced as voi
import numpy
from  scipy.io import wavfile
import pitch_mark_first_step as pmfs
import pitch_mark_second_stage as pmss


def freq_shift_using_td_psola_helper(sndarray, freq_chunk, best_pitch_marks_freq_chunk, freq, freqShiftFactor):
    best_pitch_marks_freq_chunk_sorted=  numpy.sort(best_pitch_marks_freq_chunk)
    print "freq chunk " + str(freq_chunk)
    # print sndarray[freq_chunk[0]:freq_chunk[1]+1]
    maxSndArray = numpy.max(sndarray[freq_chunk[0]:freq_chunk[1]+1])
    minSndArray = numpy.min(sndarray[freq_chunk[0]:freq_chunk[1]+1])
    # print "maxSndArray " + str(maxSndArray)
    # print "minSndArray " + str(minSndArray)
    # or (freq_chunk[0] < 15360 or freq_chunk[0] >= 16383)
    if maxSndArray <= 500 and maxSndArray >= 0 or minSndArray < 0 and minSndArray >= -500 :
        return sndarray[freq_chunk[0]:freq_chunk[1]+1]
        # return numpy.zeros(len(sndarray[freq_chunk[0]:freq_chunk[1]+1]))
    # for i in range(freq_chunk[0],freq_chunk[1]+1):
    #     if sndarray[i] <= 500 and sndarray[i]>= 0 or sndarray[i] < 0 and sndarray[i] >= -500:
    #         sndarray[i] = 0.0

    diff_pitch_marks_freq_chunk = numpy.diff(best_pitch_marks_freq_chunk_sorted)
    if len(diff_pitch_marks_freq_chunk) == 0:
        period = float(1)/float(freq)
        periodToSamps = period * 44100
        average_period = numpy.int(periodToSamps)
    else:
        average_period = numpy.average(diff_pitch_marks_freq_chunk)
    synthesis_pitch_marks = []


    prepared_segments=[]
    segments_range = []
    cnt = 0
    for i in best_pitch_marks_freq_chunk_sorted:
        if cnt != 0:
            scopeLeft = diff_pitch_marks_freq_chunk[cnt-1]
        if cnt != len(diff_pitch_marks_freq_chunk):
            scopeRight = diff_pitch_marks_freq_chunk[cnt]
        if cnt == 0:
            scopeLeft = i-freq_chunk[0]
        if cnt == len(diff_pitch_marks_freq_chunk):
            scopeRight = freq_chunk[1]-i
        leftSeg = i - scopeLeft
        rightSeg = i + scopeRight
        additional_len = numpy.abs(scopeLeft-scopeRight)

        print best_pitch_marks_freq_chunk_sorted
        print diff_pitch_marks_freq_chunk
        print "cnt " + str(cnt)
        print "best pitch mark " + str(i)
        print "scope right " + str(scopeRight)
        print "scope left " + str(scopeLeft)
        print "leftSeg " + str(leftSeg)
        print "rightSeg " + str(rightSeg)
        print "additional len " + str(additional_len)
        hanning = numpy.asarray(numpy.hanning(scopeLeft +  scopeRight + additional_len))
        if scopeRight >= scopeLeft:
            # print "I ma here 1"
            new_hanning = hanning[additional_len:]
        else:
            # print "I am here 2"
            new_hanning = hanning[0:scopeLeft+scopeRight]
        segment = numpy.asarray(sndarray[leftSeg:rightSeg])
        segmentHanning = segment * new_hanning

        start = leftSeg
        end = rightSeg
        diff = end - start
        # print len(new_hanning)
        # print new_hanning
        # print diff
        import matplotlib.pyplot as plt
        xplot = []
        for j in range(leftSeg,rightSeg):
            xplot.append(j)
        # print "i " + str(i)
        # plt.plot(i,sndarray[i],'o',markersize=10,color='red', label=" best pitch markers")
        # plt.plot(xplot,sndarray[start:end],'-o',color='blue',label="amplitude of sound")
        # plt.plot(xplot,numpy.asarray(new_hanning)*sndarray[i],'-',color='black', label='hanning')
        # plt.xlim(leftSeg,rightSeg)
        # # plt.legend()
        # plt.show()


        segments_range.append([scopeLeft,scopeRight])
        prepared_segments.append(segmentHanning)
        cnt = cnt + 1

    # print segments_range

    new_pitch_mark = best_pitch_marks_freq_chunk_sorted[0]
    new_pitch_marks =[]
    leftSegs = []
    rightSegs = []
    new_pitch = int(average_period/freqShiftFactor)
    new_snd_array = numpy.zeros(freq_chunk[1]-freq_chunk[0]+1)
    while new_pitch_mark <= freq_chunk[1]:
        new_pitch_marks.append(new_pitch_mark)
        # minimum = numpy.min(numpy.abs(numpy.asarray(best_pitch_marks_freq_chunk)-new_pitch))
        diff_array = numpy.abs(numpy.asarray(best_pitch_marks_freq_chunk_sorted)-new_pitch_mark)
        minArg = numpy.argmin(diff_array)
        scopeLeft= segments_range[minArg][0]
        scopeRight = segments_range[minArg][1]
        leftSeg = new_pitch_mark - freq_chunk[0] - scopeLeft
        rightSeg = new_pitch_mark - freq_chunk[0] + scopeRight
        # print "scopeLeft " + str(scopeLeft)
        # print "scopeRight " + str(scopeRight)
        # print "LeftSeg " + str(leftSeg)
        # print "RightSeg " + str(rightSeg)
        added_snd_array = prepared_segments[minArg]
        if(leftSeg) < 0:
            added_snd_array = prepared_segments[minArg][-leftSeg:]
            leftSeg = 0
        if(rightSeg) >= len(new_snd_array):
            len_seg = len(prepared_segments[minArg])
            len_snd = len(new_snd_array)
            added_snd_array = prepared_segments[minArg][0:(len_seg-(rightSeg-len_snd)-1)]
            rightSeg = len(new_snd_array)-1
        leftSegs.append(leftSeg+freq_chunk[0])
        rightSegs.append(rightSeg+freq_chunk[0])
        # print "min Arg array " + str(diff_array)
        # print "new_pitch_mark " + str(new_pitch_mark)
        # print "minArg " + str(minArg)
        # print "len new_snd_array_seg " + str(len(new_snd_array[leftSeg:rightSeg]))
        # print "len minArg sndarray " + str(len(added_snd_array))

        # break
        new_snd_array[leftSeg:rightSeg] = numpy.asarray(new_snd_array[leftSeg:rightSeg]) + numpy.asarray(added_snd_array)
        # synthesis_pitch_marks.append(new_pitch_mark)
        new_pitch_mark = new_pitch_mark + new_pitch

    best_pitch_marks_y = []
    for i in best_pitch_marks_freq_chunk_sorted:
        best_pitch_marks_y.append(sndarray[i])
    new_pitch_marks_y = []
    for i in new_pitch_marks:
        new_pitch_marks_y.append(0.0)
    leftSegs_y = []
    for i in leftSegs:
        leftSegs_y.append(sndarray[i])
    rightSegs_y = []
    for i in rightSegs:
        rightSegs_y.append(sndarray[i])

    start = freq_chunk[0]
    end = freq_chunk[1]+1
    diff = end - start
    best_pitch_marks_new = []
    for j in best_pitch_marks_freq_chunk_sorted:
        best_pitch_marks_new.append(j)
    new_pitch_marks_new = []
    for j in new_pitch_marks:
        new_pitch_marks_new.append(j)
    leftSegs_new = []
    for j in leftSegs:
        leftSegs_new.append(j)
    rightSegs_new = []
    for j in rightSegs:
        rightSegs_new.append(j)
    xplotTwo = []
    for i in range(start,end):
        xplotTwo.append(i)

    import matplotlib.pyplot as plt
    # print leftSegs
    # print best_pitch_marks_new
    # plt.plot(best_pitch_marks_new,best_pitch_marks_y,'x',markersize=60,color='red', label=" analysis pitch markers")
    # plt.plot(new_pitch_marks,new_pitch_marks_y,'o',markersize=10,color='black', label=" synthesis pitch markers")
    # # plt.plot(leftSegs,leftSegs_y,'o',markersize=20,color='red', label=" leftSegsStart")
    # # plt.plot(rightSegs,rightSegs_y,'o',markersize=20,color='black', label=" rightSegsStart")
    # plt.plot(xplotTwo,sndarray[start:end],'-o',color='blue',label="amplitude old sound")
    # plt.plot(xplotTwo,new_snd_array,'-',color='red',label="amplitude new sound")
    # plt.xlim(start, end)
    # # plt.legend()
    # plt.show()
    return new_snd_array
    # print average_period
    # print new_pitch

    # print synthesis_pitch_marks

def freq_shift_using_td_psola(sndarray,chunk_size,freqShiftFactor,best_pitch_marks_info,freq_chunks_info):
    # new_sndarray_zeros = numpy.zeros(len(sndarray))
    new_sndarray = []
    for i in sndarray:
        new_sndarray.append(i)
    f0 = voi.get_freq_array(new_sndarray,44100,chunk_size)
    cnt = 0
    spots = []
    print "freq_chunks_info " + str(freq_chunks_info)
    # print len(sndarray)
    for freq_chunks_region in freq_chunks_info:
        cntTwo = 0
        new_sndarray_two = []
        # print "NEW REGION STARTED!!!!!!!!!!!!!!"
        # print len(sndarray)
        for freq_chunk in freq_chunks_region:
            spot = freq_chunk[0]/chunk_size
            freq = f0[spot]

            x = freq_shift_using_td_psola_helper(sndarray,freq_chunk,best_pitch_marks_info[cnt][cntTwo],freq, freqShiftFactor)
            diff_arrays = numpy.asarray(x) - numpy.asarray(sndarray[freq_chunk[0]:freq_chunk[1]+1])

            # print "diff array " + str(diff_arrays.tolist())
            #
            # best_pitch_marks_y = []
            # for i in best_pitch_marks_info[cnt][cntTwo]:
            #     best_pitch_marks_y.append(sndarray[i])
            #
            # start = freq_chunk[0]
            # end = freq_chunk[1]
            # diff = end - start
            # best_pitch_marks_new = []
            # for j in best_pitch_marks_info[cnt][cntTwo]:
            #     best_pitch_marks_new.append(j-start)
            #
            # import matplotlib.pyplot as plt
            # plt.plot(best_pitch_marks_new,best_pitch_marks_y,'o',markersize=10,color='red', label=" best pitch markers")
            # plt.plot(y[0:diff],sndarray[start:end],'-o',color='blue')
            # plt.plot(numpy.asarray(x),'-',color='red')
            # plt.xlim(0, len(x))
            # plt.legend()
            # plt.show()
            for i in range(0,len(x)):
                spot = i + freq_chunk[0]
                # print str(spot) + " " + str(int(x[i])) + " " + str(sndarray[spot]) + " " + str(new_sndarray[spot])
                # print type(x[i])
                # if x[i] <= 200 and x[i] >= 0 or x[i] < 0 and x[i] >= -200:
                #     new_sndarray_zeros[spot] = 0.0
                # else:
                # new_sndarray_zeros[spot] = int(x[i])
                new_sndarray[spot] = numpy.int16(x[i])
                spots.append(spot)
            cntTwo = cntTwo + 1
        cnt = cnt + 1

    # new_sndarray_y = []
    # for i in spots:
    #     new_sndarray_y.append(new_sndarray[i])

    # import matplotlib.pyplot as plt

    # diff = numpy.asarray(new_sndarray) - numpy.asarray(new_sndarray_zeros)
    # print freq_chunks_info[0][0][0]
    # print diff[0:freq_chunks_info[0][0][0]].tolist()
    # print new_sndarray[0:freq_chunks_info[0][0][0]]
    # print len(new_sndarray[0:freq_chunks_info[0][0][0]])
    # print new_sndarray_zeros[0:freq_chunks_info[0][0][0]].tolist()
    # print len(new_sndarray_zeros[0:freq_chunks_info[0][0][0]].tolist())
    # plt.plot(new_sndarray_zeros,'o',markersize=5,color='red', label=" amplitude_new sound")
    # # plt.plot(x[start:end],'-',color='black',label='amplitude old sound')
    # plt.xlim(0, len(sndarray))
    # plt.legend()
    # plt.show()
    return new_sndarray

if __name__ == "__main__":
    filename= "C:/Users/rediet/Documents/Vocie-samples/amy.wav"
    filenameFreqShift = "C:/Users/rediet/Documents/Vocie-samples/ericFreqShift.wav"

    fs, x = wavfile.read(filename)
    y = numpy.arange(0,len(x),1)
    x = voi.get_one_channel_array(x)
    chunk_size = 1024

    # voi.plot(y,x,len(x),"signal amplitude")

    vSig = voi.get_signal_voiced_unvoiced_starting_info(x,fs,chunk_size)
    lengthVoiced = voi.get_signal_voiced_length_info(x,vSig)
    # lengthUnvoiced = voi.get_signal_unvoiced_length_info(x,vSig)
    #
    voiced_regions = voi.get_voiced_region_chunks(vSig,lengthVoiced)
    # unvoiced_regions = voi.get_unvoiced_region_chunks(vSig,lengthUnvoiced)
    # voiced_regions = []
    # voiced_regions.append([0,len(x)])
    print " voiced regions " + str(voiced_regions)
    pitch_marks,voiced_region_freq_chunk_windows_pitch_marks_obj = pmfs.get_pitch_marks_regions(x,voiced_regions,chunk_size, "voiced")
    best_voiced_region_freq_chunk_windows_pitch_marks_obj = pmss.optimal_accumulated_log_probability(x,voiced_region_freq_chunk_windows_pitch_marks_obj)

    best_pitch_marks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["best_pitch_marks"]
    freq_chunks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["freq_chunks"]
    new_x = freq_shift_using_td_psola(x,chunk_size,2,best_pitch_marks_info , freq_chunks_info)

    print (len(new_x))
    new_x = voi.make_two_channels(new_x)
    voi.write_to_new_file(filenameFreqShift,numpy.asarray(new_x))
    # print unvoiced_regions
    # print new_x
    #
    # start = voiced_regions[0][0]
    # end = voiced_regions[0][1]
    # diff = end - start
    #
    # import matplotlib.pyplot as plt
    #
    #
    # plt.plot(new_x[start:end],'-',markersize=10,color='red', label=" amplitude_new sound")
    # plt.plot(x[start:end],'-',color='black',label='amplitude old sound')
    # plt.xlim(0, len(x[0:diff]))
    # plt.legend()
    # plt.show()