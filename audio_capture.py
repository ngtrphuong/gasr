import pyaudio
import wave

class AudioCapture:
    def __init__(self, channels=1, rate=44100, chunk=1024):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.p = pyaudio.PyAudio()

    def start_recording(self, filename):
        self.stream = self.p.open(format=pyaudio.paInt16,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.chunk)
        print("Recording...")
        self.frames = []

        try:
            while True:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")
            self.stop_recording(filename)

    def stop_recording(self, filename):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        print(f"Audio saved as {filename}")

if __name__ == '__main__':
    audio = AudioCapture()
    audio.start_recording('output.wav')