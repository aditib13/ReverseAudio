import pyaudio
import wave
import time
import sys


if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)


index = 40*1024
wf = wave.open(sys.argv[1], 'rb')
wf.setpos(index)
p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    global index
    data = wf.readframes(frame_count)
    data = data[::-1]
    index-=1024
    wf.setpos(index)

    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)


stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()
