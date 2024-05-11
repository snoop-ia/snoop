import os
from pytube import YouTube
import time


def download_audio_from_youtube_video(video_urls, output_format="wav", output_path="../../data/audio/") -> str:
    # Ensure video_urls is a list to handle single or multiple URLs uniformly
    if isinstance(video_urls, str):
        video_urls = [video_urls]

    # Create the specific format directory if it doesn't exist
    format_path = os.path.join(output_path, output_format)
    if not os.path.exists(format_path):
        os.makedirs(format_path)


    file_paths = []

    # Process each video URL
    for i, url in enumerate(video_urls):
        start_time = time.time()
        print(f"Video {i + 1} of {len(video_urls)}: {url}")
        print(f"\nTitle: {YouTube(url).title}")
        try:
            yt = YouTube(url)
            # Get the audio stream preferring the highest quality
            stream = yt.streams.filter(only_audio=True).first()
            # Download and save the file in the specified format directory
            # Generate a filename safe string
            safe_title = "".join([c for c in yt.title if c.isalnum() or c in " -_"]).rstrip()
            filename = f"{safe_title}.{output_format}"
            stream.download(output_path=format_path, filename=filename)
            end_time = time.time()
            print(f"Download completed for {url} in {end_time - start_time} seconds")
            file_paths.append(os.path.join(format_path, filename))
        except Exception as e:
            print(f"Failed to download {url}. Reason: {str(e)}")

    if len(file_paths) == 1:
        return file_paths[0]
    else:
        return file_paths


def main():
    print(f"Starting {main.__name__}")
    # videos_url_list = ["https://www.youtube.com/watch?v=5wYyJckGrdc",
    #                    "https://www.youtube.com/watch?v=XO-F8yfYmnE",
    #                    "https://www.youtube.com/watch?v=RnT-xQCEb-E",
    #                    "https://www.youtube.com/watch?v=3D-AXpMRCXY"]

    video_url = "https://www.youtube.com/watch?v=5wYyJckGrdc"

    start_time = time.time()
    # path = download_audio_from_youtube_video(videos_url_list, output_format="wav")
    path = download_audio_from_youtube_video(video_url, output_format="wav")
    end_time = time.time()
    print(f"\nAudio file saved at: {path}")
    print(f"Total time taken: {end_time - start_time} seconds")


if __name__ == '__main__':
    main()