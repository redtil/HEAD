

from pyo import *# s = Server().boot()
import os

s = Server(nchnls=2).boot()
s.start()
mydir = 'C:/Users/rediet/Documents/Vocie-samples/'
myfile = 'amy.wav'
file = os.path.join(mydir, myfile)
sf = SfPlayer(file, speed=1, loop=False)
print sf