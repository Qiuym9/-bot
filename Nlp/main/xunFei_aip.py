# -*-coding:utf-8 -*-
import pyaudio
import wave
from Nlp.main.xunfei_text_to_voice import textToVoice

output_filePath = "./voice/output.wav"


def xunFeiAPI():
    result = textToVoice()
    # 播放生成的音频文件
    chunk = 1024
    wf = wave.open(output_filePath, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    data = wf.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return result


if __name__ == '__main__':
    xunFeiAPI()