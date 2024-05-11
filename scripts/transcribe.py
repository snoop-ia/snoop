import whisper

from utils import metadata_retriever as mr
from utils import json_dict_manip as jdm


def get_model(model_type="base"):
    print("Available models:")
    print(whisper.available_models())
    model = whisper.load_model(model_type)
    return model


def transcribe_audio(model, audio_file_path, language) -> dict:
    print("Transcribing audio...")
    transcription = whisper.transcribe(model=model,
                                       audio=audio_file_path,
                                       verbose=True,
                                       language=language
                                       )
    return transcription


def main():
    print(f"Starting {main.__name__}")

    model_type = "base"
    language = "fr"
    model = get_model(model_type)

    # audio_file_path = "../data/audio/mp3/Simone Veil  son discours historique en faveur de lIVG.mp3"
    audio_file_path = "../data/audio/wav/Simone Veil  son discours historique en faveur de lIVG.wav"

    # Get metadata
    metadata = {"metadata": mr.get_metadata(audio_file_path)}
    print(f"Metadata: {metadata}")

    transcription = transcribe_audio(model, audio_file_path, language=language)

    # Insert metadata into transcription
    transcription.update(metadata)
    print(f"Transcription with metadata: {transcription}")

    jdm.save_dict_as_json(transcription, f"../data/transcriptions/transcription_info_{model_type}.json")

    print(f"Ending {main.__name__}")


if __name__ == '__main__':
    main()
