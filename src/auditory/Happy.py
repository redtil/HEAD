from pyo import *

filename = 'C:/Users/rediet/Documents/Vocie-samples/eric.wav'
filenameInflection = 'C:/Users/rediet/Documents/Vocie-samples/ericInflectionPyo.wav'
filenameFreqShift = 'C:/Users/rediet/Documents/Vocie-samples/ericFreqShiftPyo.wav'
filenameHappy = "C:/Users/rediet/Documents/Vocie-samples/ericHappyPyo.wav"
s = Server().boot()
dur = sndinfo(filename)[1]
t2 = NewTable(length=dur)
sf2 = SfPlayer(filename, speed=1, loop=False)
pit_shift = Yin(sf2, tolerance=0.001, minfreq=60, maxfreq=300, cutoff=300, winsize=1024, mul=0.9, add=0)
b  = FreqShift(sf2, shift=50 , mul=1).out()
rec2 = TableRec(b, table=t2)
rec2.play()
s.start()
time.sleep(dur*10)
# rec2.stop()
s.stop()
savefileFromTable(t2,filenameFreqShift,0,0)



