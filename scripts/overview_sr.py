import whisper
import json


def get_model(model_type="base"):
    print("Available models:")
    print(whisper.available_models())
    model = whisper.load_model(model_type)
    return model


def transcribe_audio(model, audio_file_path, language="fr"):
    transcription = whisper.transcribe(model=model,
                                       audio=audio_file_path,
                                       verbose=True,
                                       language=language
                                       )
    print(f"Transcription: {transcription}")
    return transcription


def save_transcription(transcription, model_type):
    name = f"transcription_{model_type}.txt"
    with open(f"../data/transcriptions/{name}", "w", encoding='utf-8') as txt_file:
        txt_file.write(transcription.get('text'))
    print(f"Transcription saved as {name}")


def save_dict_as_json(dict_data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(dict_data, json_file)
    print(f"Data saved in {file_path}")


def main():
    print(f"Starting {main.__name__}")

    model_type = "small"
    model = get_model(model_type)

    # audio_file_path = "../data/audio/mp3/Simone Veil  son discours historique en faveur de lIVG.mp3"
    audio_file_path = "../data/audio/wav/Simone Veil  son discours historique en faveur de lIVG.wav"
    transcription = transcribe_audio(model, audio_file_path)

    save_dict_as_json(transcription, f"../data/transcriptions/transcription_info_{model_type}.json")
    # save_transcription(transcription, model_type)

    print(f"Ending {main.__name__}")


if __name__ == '__main__':
    main()
