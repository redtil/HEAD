

from pyo import *# s = Server().boot()
s = Server(audio='jack', nchnls=2).boot()
s.start()
file= "/home/zelalem/Documents/Vocie-samples/amy.wav"
sf = SfPlayer(file, speed=1, loop=False)