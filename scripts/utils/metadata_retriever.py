import json
import os
import wave

from mutagen.mp3 import MP3


def get_metadata(file_path, output_path=None) -> dict:
    if file_path.endswith(".mp3"):
        audio = MP3(file_path)
        metadata = {
            "File": file_path,
            "Type": "MP3",
            "Duration": audio.info.length,
            "Bytes": os.path.getsize(file_path)
        }

    elif file_path.endswith(".wav"):
        with wave.open(file_path, 'rb') as audio:
            duration = audio.getnframes() / float(audio.getframerate())
            size_bytes = audio.getnframes() * audio.getnchannels() * audio.getsampwidth()
            metadata = {
                "File": file_path,
                "Type": "WAV",
                "Duration": duration,
                "Bytes": size_bytes
            }
    else:
        metadata = {
            "File": file_path,
            "Error": "Unsupported file format"
        }

    if output_path is not None:
        with open(output_path, "w") as json_file:
            json.dump(metadata, json_file, indent=4)
        print(f"Metadata saved in {output_path}")

    return metadata


def main():
    print(f"Starting {main.__name__}")

    # Single file way, for demonstration since paths are hypothetical
    file_path = "../data/audio/wav/Simone Veil  son discours historique en faveur de lIVG.wav"
    metadata = get_metadata(file_path)
    print(metadata)

    print(f"Ending {main.__name__}")


# Note: Execution lines are commented out to prevent running in this environment.
if __name__ == '__main__':
    main()
