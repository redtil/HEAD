
import numpy
import td_psola as tp
import voiced_unvoiced as voi
import pitch_mark_first_step as pmfs
import pitch_mark_second_stage as pmss
from scipy.io import wavfile
from pyo import *


def voiced_region_to_freq_chunks(region_info,chunk_size):
    len = region_info[1] - region_info[0] + 1
    steps = int(numpy.ceil(len/chunk_size))
    freq_chunks = []
    for i in range(0,steps):
        chunk_start = i * chunk_size + region_info[0]
        if chunk_start >= region_info[1]:
            chunk_start = region_info[1]
        chunk_end = chunk_start + chunk_size - 1
        if chunk_end >= region_info[1]:
            chunk_end = region_info[1]
        freq_chunks.append([chunk_start,chunk_end])

def inflection(sndarray,voiced_regions_info, inflection_duration, fs,chunk_size):
    new_sndarray = []

    duration_to_samps = inflection_duration * fs
    no_of_freq_chunks = int(numpy.floor(duration_to_samps/chunk_size))
    # pa_list_devices()
    print pa_count_devices()


    print "duration_to_samps " + str(duration_to_samps)
    print "no_of_freq_chunks " + str(no_of_freq_chunks)
    for i in sndarray:
        new_sndarray.append(i)


    # durations = []
    win_sizes = []
    vr_ends = []
    for i in range(0,len(voiced_regions_info)):
        filename = 'C:/Users/rediet/Documents/Vocie-samples/eric500' + '-' + str(i) + '.wav'
        filenameRecord = 'C:/Users/rediet/Documents/Vocie-samples/eric500Shifted' + '-' + str(i) + '.wav'

        len_vr = voiced_regions_info[i][1] - voiced_regions_info[i][0] + 1
        vr_start = 0
        vr_end = (no_of_freq_chunks * chunk_size) - 1
        if vr_end >= len_vr:
            vr_end = len_vr - 1
        # duration = float(vr_end-vr_start+1)/float(fs)
        voiced_regions = []
        voiced_regions.append([vr_start,vr_end])

        snd_arr = sndarray[voiced_regions_info[i][0]:vr_end+ voiced_regions_info[i][0] + 1]
        winsize = 1024
        if vr_end - vr_start + 1 < 1024:
            winsize = vr_end - vr_start
        win_sizes.append(winsize)
        vr_ends.append(vr_end)
        wavfile.write(filename,fs,numpy.asarray(snd_arr))

        # print voiced_regions_info[i]
        # print voiced_regions
        # pitch_marks,voiced_region_freq_chunk_windows_pitch_marks_obj = pmfs.get_pitch_marks_regions(snd_arr,voiced_regions,chunk_size, "voiced")
        # # print voiced_region_freq_chunk_windows_pitch_marks_obj
        # best_voiced_region_freq_chunk_windows_pitch_marks_obj = pmss.optimal_accumulated_log_probability(snd_arr,voiced_region_freq_chunk_windows_pitch_marks_obj)
        # best_pitch_marks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["best_pitch_marks"]
        # freq_chunks_info = best_voiced_region_freq_chunk_windows_pitch_marks_obj["freq_chunks"]
        # new_snd = tp.freq_shift_using_td_psola(snd_arr,chunk_size,1.5,best_pitch_marks_info , freq_chunks_info)
        # # print "new_snd " + str(new_snd)
        #
        # start = voiced_regions_info[i][0]
        # for i in range(0,len(new_snd)):
        #     new_sndarray[i+start] = new_snd[i]

    pit_shifts = []
    s = Server()
    s.boot()
    for i in range(0,len(voiced_regions_info)):
        filename = 'C:/Users/rediet/Documents/Vocie-samples/eric500' + '-' + str(i) + '.wav'
        filenameRecord = 'C:/Users/rediet/Documents/Vocie-samples/eric500Shifted' + '-' + str(i) + '.wav'
        dur = sndinfo(filename)[1]
        # print "dur " + str(dur)
        # duration_to_samps = dur* fs
        # no_of_freq_chunks = int(numpy.floor(duration_to_samps/chunk_size))
        # print "freq_chunks " + str(no_of_freq_chunks)
        winsize = win_sizes[i]
        # t = NewTable(length=dur)
        sf = SfPlayer(filename, interp= 1, speed=1, loop=False)
        pit_shift = Yin(sf, tolerance=0.001, minfreq=60, maxfreq=300, cutoff=300, winsize=winsize, mul=0.9, add=0)
        # rec = TableRec(pit_shift, table=t)
        # rec.play()
        # s.start()
        # time.sleep(dur*4)
        # s.stop()
        pit_shifts.append(pit_shift)


        # print numpy.asarray((numpy.asarray(t.getTable())/3.0517578125e-05)).tolist()
        # print numpy.asarray(numpy.asarray(SndTable(filename).getTable())/3.0517578125e-05).tolist()
        # print str(numpy.asarray((numpy.asarray(t.getTable()))).tolist())
        # t_cp = []
        # cnt = 0
        # for i in t.getTable():
        #     if cnt % 1025 == 0:
        #         t_cp.append(i)
        #     cnt = cnt + 1
        # savefileFromTable(t,filenameRecord,0,0)
        # print numpy.unique(t.getTable(),True,return_counts = True)
        # print t.getTable()
        # print len(t_cp)
        # print t_cp

    s = Server()
    s.boot()
    for i in range(0,len(voiced_regions_info)):
        filename = 'C:/Users/rediet/Documents/Vocie-samples/eric500' + '-' + str(i) + '.wav'
        filenameRecord = 'C:/Users/rediet/Documents/Vocie-samples/eric500Shifted' + '-' + str(i) + '.wav'

        pit_shift = pit_shifts[i]
        # print pit_shift
        # print filename
        # duration = durations[i]
        # print duration
        dur = sndinfo(filename)[1]

        t2 = NewTable(length=dur)
        sf2 = SfPlayer(filename, speed=1, loop=False)
        b  = FreqShift(sf2, shift=40 , mul=1).out()
        rec2 = TableRec(b, table=t2)
        rec2.play()
        s.start()
        time.sleep(dur*4)
        rec2.stop()

        # sf = SfPlayer(filename, speed=1, loop=False).out()

        # print t2.getTable()
        savefileFromTable(t2,filenameRecord,0,0)
    s.stop()
    for i in range(0,len(voiced_regions_info)):
        filename = 'C:/Users/rediet/Documents/Vocie-samples/eric500' + '-' + str(i) + '.wav'
        filenameRecord = 'C:/Users/rediet/Documents/Vocie-samples/eric500Shifted' + '-' + str(i) + '.wav'
        # print " filename " + str(filenameRecord)
        fs, new_snd = wavfile.read(filenameRecord)

        print len(new_snd)
        # print new_snd.tolist()
        vr_end = vr_ends[i]
        start = voiced_regions_info[i][0]
        for i in range(0,len(new_snd)):
            new_sndarray[i+start] = new_snd[i]
    return new_sndarray
if __name__ == "__main__":
    filename= "C:/Users/rediet/Documents/Vocie-samples/eric.wav"
    filenameInflection = "C:/Users/rediet/Documents/Vocie-samples/ericInflectionPyo.wav"
    filenameTxt = "C:/Users/rediet/Documents/Vocie-samples/ericInflection.txt"

    fs, x = wavfile.read(filename)
    y = numpy.arange(0,len(x),1)
    x = voi.get_one_channel_array(x)
    chunk_size = 1024

    # voi.plot(y,x,len(x),"signal amplitude")

    vSig = voi.get_signal_voiced_unvoiced_starting_info(x,fs,chunk_size)
    lengthVoiced = voi.get_signal_voiced_length_info(x,vSig)
    # lengthUnvoiced = voi.get_signal_unvoiced_length_info(x,vSig)

    voiced_regions = voi.get_voiced_region_chunks(vSig,lengthVoiced)

    new_snd = inflection(x,voiced_regions,0.5,fs,chunk_size)
    new_snd_new = []
    print
    cnt = 0
    for i in new_snd:
        # print str(cnt) + " " + str(len(new_snd))
        new_snd_new.append(numpy.int16(i))
        if cnt == len(new_snd)-1:
            break
        cnt = cnt + 1
        # print new_snd_new
    # print new_snd
    # print len(new_snd)
    # numpy.savetxt(filenameTxt,new_snd)
    wavfile.write(filenameInflection,fs,numpy.array(new_snd_new))
    # new_snd = voi.make_two_channels(new_snd)
    # voi.write_to_new_file(filenameInflection,numpy.asarray(new_snd_new))



