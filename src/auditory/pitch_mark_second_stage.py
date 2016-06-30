from scipy.io import wavfile
import numpy
import voiced_unvoiced as voi
import pitch_mark_first_step as pmfs

def calculate_state_probability(hcanditate, hmax, hmin):
    num = hcanditate - hmin
    den = hmax - hmin

    quo = float(num)/float(den)
    return quo

def get_state_probabilities(sndarray,pitch_marks_freq_array,wind, cand,hmax, hmin):
    state_prob = []
    state_prob_wind_cand = calculate_state_probability(sndarray[pitch_marks_freq_array[wind][cand]],hmax,hmin)
    for i in pitch_marks_freq_array[wind]:
        state_prob.append(calculate_state_probability(sndarray[i],hmax,hmin))
    summ = numpy.sum(state_prob)
    norm = float(state_prob_wind_cand)/float(summ)
    return norm

def calculate_transition_probability(beta,fs,dist):
    fs = float(fs)
    dist = float(dist)
    freq = dist/fs
    den = 1 + (beta * numpy.abs(freq-fs/dist))
    num = 1
    quo = num/den
    return quo

def get_transition_probabilities(sndarray,pitch_marks_freq_array,wind,fs, candOne,candTwo, beta):
    trans_prob = []
    dist = pitch_marks_freq_array[wind+1][candOne] - pitch_marks_freq_array[wind][candTwo]
    trans_prob_wind_cand = calculate_transition_probability(beta,fs,dist)
    for i in pitch_marks_freq_array[wind+1]:
        dist = i - pitch_marks_freq_array[wind][candOne]
        trans_prob.append(calculate_transition_probability(beta,fs,dist))
    summ = numpy.sum(trans_prob)
    norm = float(trans_prob_wind_cand)/float(summ)
    return norm

def optimal_accumulated_log_probability_recur_helper(sndarray,pitch_marks_freq_array,identifier, helper_array, hmax, hmin,fs):
    retVal = []
    opt = []
    cnt = 0
    pitchMarksCnt = len(pitch_marks_freq_array[0])
    for i in pitch_marks_freq_array[identifier]:
        candState = get_state_probabilities(sndarray,pitch_marks_freq_array,identifier,cnt,hmax,hmin)
        if identifier == 0:
            opt.append(candState)
            helper_array[cnt + identifier*pitchMarksCnt] = candState
        else:
            cntTwo = 0
            beta = 0.7
            optTwo = []
            for i in pitch_marks_freq_array[identifier-1]:
                if helper_array[cntTwo + identifier-1 * pitchMarksCnt] != numpy.NaN:
                    prev_opt = helper_array[cntTwo + identifier-1 * pitchMarksCnt]
                else:
                    optimal_accumulated_log_probability_recur_helper(sndarray,pitch_marks_freq_array,identifier-1,helper_array,hmax,hmin,fs)
                    prev_opt = helper_array[cntTwo + identifier-1 * pitchMarksCnt]
                trans_prob = get_transition_probabilities(sndarray,pitch_marks_freq_array,identifier-1,fs,cntTwo,cnt,beta)
                optTwo.append( prev_opt + trans_prob )
            maxK = numpy.argmax(optTwo)
            retVal.append(maxK)
            summ = optTwo[maxK] + candState
            helper_array[cnt + identifier* pitchMarksCnt] = summ
            opt.append(summ)
        cnt = cnt + 1
    maxOpt = numpy.argmax(opt)
    if identifier == len(pitch_marks_freq_array) - 1:
        retVal.append(maxOpt)
    return retVal

def optimal_accumulated_log_probability_recur(sndarray,pitch_marks_freq_chunk, hmax, hmin,fs):
    pitchMarksCnt = len(pitch_marks_freq_chunk[0])
    helper_array_len = len(pitch_marks_freq_chunk) * pitchMarksCnt
    helper_array = numpy.empty(helper_array_len,int)
    helper_array[:] = numpy.NAN
    identifier = len(pitch_marks_freq_chunk)-1
    return optimal_accumulated_log_probability_recur_helper(sndarray,pitch_marks_freq_chunk,identifier,helper_array,hmax,hmin,fs)


def optimal_accumulated_log_probability(sndarray, all_snd_info):
    best_voiced_region_freq_chunk_windows_pitch_marks_obj = {"voiced_region":[],"freq_chunks":[],"windows":[],"pitch_marks":[],"best_pitch_marks":[]}
    cnt = 0
    new_snd_info = all_snd_info
    best_voiced_region_freq_chunk_windows_pitch_marks_obj["voiced_region"] = new_snd_info["voiced_region"]
    best_voiced_region_freq_chunk_windows_pitch_marks_obj["freq_chunks"] = new_snd_info["freq_chunks"]
    best_voiced_region_freq_chunk_windows_pitch_marks_obj["windows"] = new_snd_info["windows"]
    best_voiced_region_freq_chunk_windows_pitch_marks_obj["pitch_marks"] = new_snd_info["pitch_marks"]

    cntVoicedRegions = 0
    for pitch_marks_voiced_region in all_snd_info["pitch_marks"]:
        best_pitch_marks_freq_chunks = []
        voiced_region_start = best_voiced_region_freq_chunk_windows_pitch_marks_obj["voiced_region"][cntVoicedRegions][0]
        voiced_region_end = best_voiced_region_freq_chunk_windows_pitch_marks_obj["voiced_region"][cntVoicedRegions][1]
        hmaxIndex = numpy.max(sndarray[voiced_region_start:voiced_region_end])
        hminIndex = numpy.min(sndarray[voiced_region_start:voiced_region_end])
        hmax = sndarray[hmaxIndex]
        hmin = sndarray[hminIndex]
        for pitch_marks_freq_chunk in pitch_marks_voiced_region:
            x = optimal_accumulated_log_probability_recur(sndarray,pitch_marks_freq_chunk,hmax,hmin,44100)
            best_pitch_marks = []
            for i in range(0,len(x)):
                for j in range(0,len(pitch_marks_freq_chunk)):
                    # print pitch_marks_freq_chunk[j][i]
                    best_pitch_marks.append(pitch_marks_freq_chunk[j][i])
            # print best_pitch_marks
            best_pitch_marks_freq_chunks.append(best_pitch_marks)
        # print best_pitch_marks_freq_chunks
        best_voiced_region_freq_chunk_windows_pitch_marks_obj["best_pitch_marks"].append(best_pitch_marks_freq_chunks)
        cntVoicedRegions = cntVoicedRegions + 1
    return best_voiced_region_freq_chunk_windows_pitch_marks_obj

if __name__ == "__main__":
    filename= "C:/Users/rediet/Documents/Vocie-samples/kendraVU500.wav"

    fs, x = wavfile.read(filename)
    y = numpy.arange(0,len(x),1)
    x = voi.get_one_channel_array(x)
    chunk_size = 80

    # voi.plot(y,x,len(x),"signal amplitude")

    vSig = voi.get_signal_voiced_unvoiced_starting_info(x,44100,chunk_size)
    lengthVoiced = voi.get_signal_voiced_length_info(x,vSig)
    voiced_regions = voi.get_voiced_region_chunks(vSig,lengthVoiced)
    pitch_marks,voiced_region_freq_chunk_windows_pitch_marks_obj = pmfs.get_pitch_marks_regions(x,voiced_regions,chunk_size, "voiced")
    best_voiced_region_freq_chunk_windows_pitch_marks_obj = optimal_accumulated_log_probability(x,voiced_region_freq_chunk_windows_pitch_marks_obj)
    print best_voiced_region_freq_chunk_windows_pitch_marks_obj

    best_pitch_marks = []
    for best_pitch_marks_voiced_region in best_voiced_region_freq_chunk_windows_pitch_marks_obj["best_pitch_marks"]:
        for best_pitch_marks_chunk in best_pitch_marks_voiced_region:
            for i in best_pitch_marks_chunk:
                best_pitch_marks.append(i)

    best_pitch_marks  = best_pitch_marks[10000:30000]
    best_pitch_marks_y = []
    for i in best_pitch_marks:
        best_pitch_marks_y.append(x[i])

    import matplotlib.pyplot as plt
    plt.plot(best_pitch_marks,best_pitch_marks_y,'x',markersize=10,color='red', label=" best pitch markers")
    plt.plot(y[0:20000],x[10000:30000],'-',color='black')
    plt.xlim(0, len(x))
    plt.legend()
    plt.show()