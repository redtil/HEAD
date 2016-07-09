from pyo import *
filename = 'C:/Users/rediet/Documents/Vocie-samples/ericInflectionPyo.wav'
filenameRecord = 'C:/Users/rediet/Documents/Vocie-samples/ericFreqShiftPyo.wav'
filenameHappy = "C:/Users/rediet/Documents/Vocie-samples/ericHappyPyo.wav"
s = Server().boot()
dur = sndinfo(filenameRecord)[1]
sf = SfPlayer(filenameRecord, speed=1, loop=False)
t = NewTable(length=dur)
# out = EQ(sf, freq=8000, q=200, boost=-3, type=2).out()
out = Atone(sf, 8000).out()
rec = TableRec(out, table=t)
rec.play()
s.start()
time.sleep(dur*4)
# rec.stop()
s.stop()
savefileFromTable(t,filenameHappy,0,0)
