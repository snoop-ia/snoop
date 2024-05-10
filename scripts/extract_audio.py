import whisper
import numpy as np


def load_audio_file(audio_path):
    """TODO"""


def load_model(model_name="medium"):
    return whisper.load_model(model_name)


def transcribe(model, audio, language="fr"):
    options = {
        "language": language,  # Specify the French language
    }
    print("Transcribing audio...")
    text_transcribe = model.transcribe(audio,  # Path to the audio file
                                       fp16=False,  # Use 16-bit floating point precision
                                       verbose=True  # Print the progress of the transcription
                                       )
    print("Transcription completed!")
    return text_transcribe["text"]


def save_transcription(transcription, file_path="../transcription.txt"):
    print("Saving transcription...")
    with open(file_path, "w", encoding='utf-8') as txt_file:
        txt_file.write(transcription)


def main():
    audio_path = "../audio_whatsapp.wav"
    load_audio_file(audio_path)
    whisper_model = load_model()
    save_transcription(transcribe(whisper_model, audio_path))


if __name__ == '__main__':
    main()
