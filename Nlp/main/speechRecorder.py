# -*-coding:utf-8 -*-
import wave
from pyaudio import PyAudio, paInt16
import time
import threading
import numpy as np
signal = 'y'   # 创建标志位


def record():
    global signal
    CHUNK = 2000
    FORMAT = paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 60               # 理论上可以设置任意数值，一定要足够大于你实际工作中需要录音的最大时长
    WAVE_INPUT_FILENAME = "./voice/input.wav"
 
    p = PyAudio()
 
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
 
    frames = []
    begin = time.time()
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if signal == 'n':     # 通过判断标志位的状态来决定何时结束录音
            break
        data = stream.read(CHUNK)
        frames.append(data)
    end = time.time()
    print('录音结束，时长为: %s 秒' % round((end - begin), 2))
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_INPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    wav_to_pcm(WAVE_INPUT_FILENAME)


def run():
    global signal
    t = threading.Thread(target=record, )   # 创建一个录音的线程
    t.start()
    signal = 'y'        # 录音结束之后恢复标志位


def stop():
    global signal
    signal = 'n'        # 改变标志位来随时结束录音


def wav_to_pcm(wav_filePath):
    # 将生成的wav格式文件转为pcm格式
    f = open(wav_filePath, 'rb')
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype=np.int16)
    wav = wav_filePath.split(".")
    wav = wav[1]
    data.tofile("." + wav + ".pcm")   # latestSpeech/input.pcm



