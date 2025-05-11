import collections
import pyaudio
import webrtcvad
import numpy as np
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
FRAME_DURATION = 30  # ms
CHUNK_SIZE = int(RATE * FRAME_DURATION / 1000)  # number of samples per frame
SILENCE_TIMEOUT = 1.0  # seconds of silence before stopping

def record_audio(filename="temp.wav"):
    vad = webrtcvad.Vad()
    vad.set_mode(1)  # 0: least aggressive, 3: most aggressive

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK_SIZE)

    ring_buffer = collections.deque(maxlen=int(400 / FRAME_DURATION))  # buffer to collect some frames before speech
    voiced_frames = []
    started = False
    silence_counter = 0

    print("Listening...")

    try:
        while True:
            frame = stream.read(CHUNK_SIZE)
            is_speech = vad.is_speech(frame, RATE)

            if not started and is_speech:
                started = True
                print("Recording...")

            if started:
                voiced_frames.append(frame)
                if is_speech:
                    silence_counter = 0
                else:
                    silence_counter += FRAME_DURATION / 1000.0
                    if silence_counter > SILENCE_TIMEOUT:
                        break

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    print("Recording complete.")

    # Save to file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(voiced_frames))
    wf.close()

    return filename
