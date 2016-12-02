import wavio
from pydub import AudioSegment
from os import listdir, remove
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read


def split(path, filename, period=5):
    Wav = wavio.read(path + filename)
    array = Wav.data
    if array.shape[1] == 2:
        array = np.sum(array, axis=1) / 2
        array = np.reshape(array, (array.shape[0], 1))
    rate = Wav.rate
    samplewidth = Wav.sampwidth
    totalTime = array.shape[0] / rate
    for i in range(totalTime / period):
        tmp = array[i * rate * period:(i + 1) * rate * period, :]
        write(tmp, filename + '_split_' + str(i) + '.wav', samplewidth=samplewidth)


def splitToTxt(path, filename):
    Wav = wavio.read(path + filename)
    array = Wav.data
    if array.shape[1] == 2:
        array = np.sum(array, axis=1) / 2
        array = np.reshape(array, (array.shape[0], 1))
    rate = Wav.rate
    sampelwidth = Wav.sampwidth
    lineWidth = 50
    f = open('txt/' + filename[0:-4] + '.txt', 'w')
    print filename[0:-4]
    for i in range(0, array.shape[0], 50):
        end = array.shape[0] if i + 50 > array.shape[0] else i + 50
        tmp = array[i:end, 0]
        str_ = ' '.join([str(t) for t in tmp])
        # print str_
        f.write(str_ + '\n')
    f.close()


def write(array, filename, rate=44100, samplewidth=4):
    filename = 'output/' + filename
    if os.path.exists(filename):
        remove(filename)
    wavio.write(filename, array, rate, sampwidth=samplewidth)


def mix(files, outputName='mix.wav'):
    output = AudioSegment.from_wav('source/' + files[0])
    for i in range(1, len(files)):
        tmp = AudioSegment.from_wav('source/' + files[i])
        output = output.overlay(tmp)
    if os.path.exists('mix/' + outputName):
        remove('mix/' + outputName)
    output.export('mix/' + outputName, format='wav')


def isVoice(filename):
    filename = filename.lower()
    dict = ['alto', 'soprano', 'tenor', 'bass', ]
    for substr in dict:
        if substr in filename:
            return True
    return False


def isInstrument(filename):
    filename = filename.lower()
    dict = ['piano', ]
    for substr in dict:
        if substr in filename:
            return True
    return False


def mixVoice(path):
    files = []
    for f in listdir(path):
        if isVoice(f):
            files.append(f)
    mix(files, 'voice.wav')


def mixNonVoice(path):
    files = []
    for f in listdir(path):
        if isInstrument(f):
            files.append(f)
    mix(files, 'nonvoice.wav')


def drawWAVPic(filename):
    # spf = wave.open(filename, 'r')
    # signal = spf.readframes(-1)
    # signal = np.fromstring(signal, 'Int16')
    # fs = spf.getframerate()
    # Time = np.linspace(0, len(signal) / fs, num=len(signal))
    # print len(Time)
    #
    # plt.title('Signal Wave...')
    # plt.plot(signal)
    # plt.show()
    (fs,x)=read(filename)
    plt.plot(x)
    plt.show()


if __name__ == "__main__":
    # mixVoice('source/')
    # mixNonVoice('source/')
    # split('mix/','voice.wav')
    # split('mix/','nonvoice.wav')
    # splitToTxt('mix/', 'voice.wav')
    # splitToTxt('mix/','nonvoice.wav')
    drawWAVPic('output/voice.wav_split_0.wav')
