import vosk
import sys
import os
import wave
import pyaudio

def recognize_voice(model_path, sample_rate=16000):
    # Initialize Vosk model
    if not os.path.exists(model_path):
        print(f"Vosk model not found at {model_path}")
        return

    vosk_model = vosk.Model(model_path)

    # Initialize PyAudio for audio input
    p = pyaudio.PyAudio()

    # Open the microphone for input
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)

    recognizer = vosk.KaldiRecognizer(vosk_model, sample_rate)

    print("Listening...")

    try:
        while True:
            data = stream.read(1024)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                recognized_text = str(result)
                print(f"Recognized: {recognized_text}")
    except KeyboardInterrupt:
        pass

    print("Recognition finished.")

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    model_path = "/home/aromal/vosk-model-small-en-us-0.15"
    recognize_voice(model_path)
