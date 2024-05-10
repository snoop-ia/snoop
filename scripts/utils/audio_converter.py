from pydub import AudioSegment
import os


def convert_audio(input_file: str, output_format: str = "wav", output_path: str = None) -> None:
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


def main():
    print(f"Starting {main.__name__}")
    input_file = "../../data/audio/wav/Sportif de haut-niveau  la gloire et largent vraiment.wav"
    # Enter the desired output format (e.g., 'mp3', 'wav')
    convert_audio(input_file, output_format="mp3")
    print(f"Ending {main.__name__}")


if __name__ == "__main__":
    main()
