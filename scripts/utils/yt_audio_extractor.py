import os
from pytube import YouTube
import time


def download_audio_from_youtube_video(video_urls, output_format="wav", output_path="../../data/audio/"):
    # Ensure video_urls is a list to handle single or multiple URLs uniformly
    if isinstance(video_urls, str):
        video_urls = [video_urls]

    # Create the specific format directory if it doesn't exist
    format_path = os.path.join(output_path, output_format)
    if not os.path.exists(format_path):
        os.makedirs(format_path)

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
        except Exception as e:
            print(f"Failed to download {url}. Reason: {str(e)}")


def main():
    print(f"Starting {main.__name__}")
    videos_url_list = ["https://www.youtube.com/watch?v=FgzM3zpZ55o",
                       "https://www.youtube.com/watch?v=E3f2Camj0Is",
                       "https://www.youtube.com/watch?v=dRIhrn8cc9w",
                       "https://www.youtube.com/watch?v=j080VBVGkfQ",
                       "https://www.youtube.com/watch?v=buptHUzDKcE",
                       "https://www.youtube.com/watch?v=gOV8-bC1_KU",
                       "https://www.youtube.com/watch?v=V7CY68zH6ps",
                       "https://www.youtube.com/watch?v=8LEuyYXGQjU",
                       "https://www.youtube.com/watch?v=E-_ecpD5PkE",
                       "https://www.youtube.com/watch?v=o_i5F1zGPLs",
                       "https://www.youtube.com/watch?v=RN8qpSs8ozY",
                       "https://www.youtube.com/watch?v=jJ7JbQBTChM",
                       "https://www.youtube.com/watch?v=Hg_uyWezMM0",
                       "https://www.youtube.com/watch?v=zPU1SRHuAW8",
                       "https://www.youtube.com/watch?v=vDF1BYWhqL8"
                       ]

    start_time = time.time()
    download_audio_from_youtube_video(videos_url_list, output_format="wav")
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")


if __name__ == '__main__':
    main()
