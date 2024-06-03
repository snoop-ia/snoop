from speech_recognition import sr


def main():
    print(f"Starting {main.__name__}")

    audio_file_path = "../data/audio/mp3/Simone Veil  son discours historique en faveur de lIVG.mp3"
    model_type = "base"

    transcription = sr.speech_recognition(audio_file_path, model_type)

    print(f"Finished {main.__name__}")


if __name__ == '__main__':
    main()
