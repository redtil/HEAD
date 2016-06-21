import wave, struct, math
import array
# from scipy.io import wavfile

baseband = wave.open("C:/Users/rediet/Documents/Vocie-samples/amy.wav", "r")
fs = baseband.getframerate()
fs = float(fs)
channel = baseband.getnchannels()
sampwidth = baseband.getsampwidth()
FM_BAND = 100
FM_CARRIER = 8.5


fm = wave.open("C:/Users/rediet/Documents/Vocie-samples/amyFM.wav", "w")
fm.setnchannels(1)
fm.setsampwidth(2)
fm.setframerate(fs)

integ_base = 0
for n in range(0, baseband.getnframes()):
    base = array.array('h', baseband.readframes(1))
    # Base signal is integrated (not mandatory, but improves
    # volume at demodulation side)
    integ_base += (base[0] + base[1])/32768.0
    # The FM trick: time (n) is multiplied only by carrier freq;
    # the frequency deviation is added afterwards.
    signal_fm = math.cos(2 * math.pi * FM_CARRIER * (n /fs) +
                         2 * math.pi * FM_BAND * integ_base / fs)
    fm.writeframes(struct.pack('h', signal_fm *32767))