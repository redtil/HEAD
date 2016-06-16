__author__ = 'zelalem'
# #
import time
import numpy, pygame.mixer, pygame.sndarray
from scikits.samplerate import resample

pygame.mixer.init(35000, -16, 2, 512)
sound_file = "/home/zelalem/emotion_dataset/OAF_witch_neutral.wav"
sound = pygame.mixer.Sound(sound_file)
snd_array = pygame.sndarray.array(sound)
# print snd_array
snd_resample = resample(snd_array, 1.9, "sinc_best").astype(snd_array.dtype) #sinc_fastest
# print snd_resample
# take the resampled array, make it an object and stop playing after 2 seconds.
snd_out = pygame.sndarray.make_sound(snd_resample)
snd_out.play()
time.sleep(5)

