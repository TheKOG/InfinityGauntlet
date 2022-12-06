import wave
import pyaudio
import os
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1
tot=60
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
channels=CHANNELS,
rate=RATE,
input=True,
frames_per_buffer=CHUNK)

def Record(filename,debug=True):
    if debug:
        print("* recording "+filename)
    frames = []
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    if debug:
        print("* done recording")
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__=='__main__':
    t=0
    for i in range(114514):
        filename="audios/snaps/snap{0}.wav".format(i)
        if(os.path.exists(filename)):
            continue
        Record(filename)
        t+=1
        if(t==tot):
            break

    stream.stop_stream()
    stream.close()
    p.terminate()