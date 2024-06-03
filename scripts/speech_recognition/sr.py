import os.path
import whisper
import datetime
import json

from typing import List, Optional

from scripts.utils import file_management as fm


def get_model(model_name="base"):
    """
    This function is used to load a specific Whisper model based on the provided model name.

    Parameters:
    model_name (str): The name of the Whisper model to load. Default is "base".

    Returns:
    model: The loaded Whisper model if the model name is valid, otherwise None.

    Raises:
    Prints an error message and returns None if the model name is not valid.

    """
    available_models = ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium',
                        'large-v1', 'large-v2', 'large-v3', 'large']

    if model_name in available_models:
        return whisper.load_model(model_name)
    else:
        print(f"Error: Model '{model_name}' is not available. Please choose from the following models : "
              f"{', '.join(model for model in available_models)}")
        return None


def transcribe(model, audio_file_path, language="fr") -> dict:
    print(f"Transcribing the audio file '{os.path.basename(audio_file_path)}'| Language '{language}'")
    transcription = whisper.transcribe(model=model,
                                       audio=audio_file_path,
                                       verbose=True,
                                       language=language
                                       )
    print("\nTranscription successfully!")
    return transcription


def save_transcription(transcription, file_type="txt"):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    name = f"transcription_{current_time}.{file_type}"

    if file_type == "json":
        fm.save_dict_as_json(transcription, f"../../data/transcriptions/{name}")
        return

    fm.save_text(transcription.get('text'), f"../../data/transcriptions/{name}")


def speech_recognition(audio_file_path: str,
                       model_type: str = "base",
                       save_speech_as: Optional[str] = None,
                       language: Optional[str] = None) -> dict:
    """
    This function performs speech recognition on an audio file using the Whisper model.

    Parameters:
    audio_file_path (str): The path to the audio file to transcribe.
    model_type (str, optional): The type of Whisper model to use for transcription. Defaults to "base".
    save_speech_as (str, optional): The format to save the transcription as. Can be "txt" or "json". Defaults to "txt".
    language (str, optional): The language of the audio file. If not provided, the Whisper model will attempt to detect the language.

    Returns:
    dict: A dictionary containing the transcription of the audio file and its metadata.

    Raises:
    Returns None if the specified model type is not available.
    """
    model = get_model(model_type)
    if model is None:
        return

    transcription = transcribe(model, audio_file_path, language)

    metadata = fm.get_metadata(audio_file_path)

    transcription = {**metadata, **transcription}

    # Save the transcription
    if save_speech_as is not None:
        save_transcription(transcription, save_speech_as)

    return transcription


def main():
    print(f"Starting {main.__name__}")

    model_name = "base"
    audio_file_path = "../../data/audio/mp3/Simone Veil  son discours historique en faveur de lIVG.mp3"
    language = "fr"

    model = get_model(model_name)
    if model is None:
        return

    transcription = transcribe(model, audio_file_path, language)

    # Get metadata
    metadata = fm.get_metadata(audio_file_path)

    # Add metadata to the transcription
    transcription = {**metadata, **transcription}

    # Save the transcription
    # save_speech(transcription, "json")

    print(f"Ending {main.__name__}")


if __name__ == '__main__':
    main()
