import os
import json
import wave

from pydub import AudioSegment
from mutagen.mp3 import MP3


def convert_audio(input_file: str,
                  output_format: str = "wav",
                  output_path: str = None) -> None:
    # If end of file is the same as the output format, return
    if os.path.splitext(input_file)[1][1:] == output_format:
        print(f"Audio is already in {output_format} format")
        return

    # Determine the format of the input file
    input_format = os.path.splitext(input_file)[1][1:]

    # Load the audio file
    audio = AudioSegment.from_file(input_file, format=input_format)

    # Output directory path based on output format
    if output_path is not None:
        output_dir = output_path
    else:
        output_dir = f"../../data/audio/{output_format}/"

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Output file path
    output_file = output_dir + os.path.splitext(os.path.basename(input_file))[0] + '.' + output_format

    # Export the audio file in the desired format
    audio.export(output_file, format=output_format)

    print(f"Audio converted to {output_format} format and saved as {output_file}")


def get_metadata(file_path, output_path=None) -> dict:
    """
    This function retrieves metadata from an audio file. It supports MP3 and WAV file formats.

    Parameters:
    file_path (str): The path to the audio file.
    output_path (str, optional): The path where the metadata will be saved as a JSON file. If not provided, the metadata will not be saved to a file.

    Returns:
    dict: A dictionary containing the metadata of the audio file. The dictionary includes the file path, file type, duration of the audio, and size in bytes. If the file format is not supported, the dictionary will include an error message.

    """
    if file_path.endswith(".mp3"):
        audio = MP3(file_path)
        metadata = {
            "Name": os.path.basename(file_path),
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


def save_dict_as_json(dict_data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(dict_data, json_file)
    print(f"Data saved in {file_path}")


def save_text(transcription_text, file_path="../../data/transcriptions/transcription.txt"):
    print("Saving transcription...")
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(transcription_text)
    print(f"Transcription saved as {file_path}")


def main():
    print(f"Starting {main.__name__}")
    input_file = "../../data/audio/mp3/Simone Veil  son discours historique en faveur de lIVG.mp3"
    # Enter the desired output format (e.g., 'mp3', 'wav')
    convert_audio(input_file, output_format="wav")
    print(f"Ending {main.__name__}")


if __name__ == "__main__":
    main()
