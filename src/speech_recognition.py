from faster_whisper import WhisperModel
import sounddevice as sd
import tempfile
import scipy.io.wavfile as wav


class VoiceInput:
    def __init__(self, model_size="base", device="cpu"):
        self.model = WhisperModel(model_size, device=device)

    def record_audio(self, duration=5, sample_rate=16000):
        print("Speak now...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
        sd.wait()
        print("Recording done.")
        return sample_rate, audio

    def save_to_wav(self, sample_rate, audio_data):
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(temp.name, sample_rate, audio_data)
        return temp.name

    def transcribe_audio(self, file_path):
        try:
            segments, info = self.model.transcribe(file_path, language="en")
            if hasattr(info, 'language') and info.language != "en":
                print("Non-English detected.")
                return None

            transcription = " ".join(segment.text.strip() for segment in segments if segment.text.strip())
            return transcription if transcription else None
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

    def listen_and_transcribe(self, duration=5):
        fs, audio = self.record_audio(duration)
        wav_path = self.save_to_wav(fs, audio)
        return self.transcribe_audio(wav_path)


def listen():
    print("Hello, welcome home...")
    recognizer = VoiceInput(model_size="base")
    print("Recognizer ready...")
    print("Ready to listen...")
    text = recognizer.listen_and_transcribe(duration=5)
    print(f"You said: {text}")
    return text
