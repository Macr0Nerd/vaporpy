from random import seed, randint
from time import time_ns
from numpy import mean, asarray
import soundfile as sf
from PIL import Image
import cv2.cv2 as cv2
from tqdm.auto import tqdm


FRAMERATE = 12
WIDTH = 1280
HEIGHT = 720
FCC = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
ALPHA = 254

seed(time_ns())

samples, rate = sf.read("JeSais.wav", always_2d=True)

samples = samples[:2500]

data = [int(((mean(x) * rate) % 255)) for x in samples]

frames = []

img = Image.new('RGBA', (WIDTH, HEIGHT), color=(data[0], data[1], data[2], 255))

frames.append(img)

with tqdm(total=len(samples)) as pbar:
    pbar.update()

    for i in data[1:]:
        current = list(img.getcolors(1)[0][-1])
        current[3] = ALPHA
        rgb = randint(0, 2)
        current[rgb] = i
        acom = Image.new('RGBA', (WIDTH, HEIGHT), color=tuple(current))
        img = Image.alpha_composite(img, acom)
        frames.append(img)
        pbar.update()

print(len(frames))

vid = None

try:
    vid = cv2.VideoWriter("test.mp4", FCC, FRAMERATE, (WIDTH, HEIGHT))
    for x in frames[:180]:
        vid.write(cv2.cvtColor(asarray(x), cv2.COLOR_RGBA2BGR))
finally:
    vid.release()
