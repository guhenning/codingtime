from pytube import YouTube
import os

# You must have pytube installed:
# to install it use the command pip install pytube
# Run the code and when asked paste or tyoe the Youtube Video URL ex.: https://www.youtube.com/watch?v=IOqxarVWKRs&pp=ygUUdGhlIHBpcmF0ZSBi0LB5IHNvbmc%3D
# The Video will be download to the Download folder on your system

# Get video url
yt_url = input("Enter the YouTube video URL: ")

video_to_download = YouTube(yt_url)

# Get video title
title = title = video_to_download.title


# Get the stream with the highest resolution
stream = video_to_download.streams.get_highest_resolution()

# Determine the download folder based on the operating system
download_folder = os.path.expanduser("~")  # Default home directory

if os.name == "posix":  # macOS or Linux
    download_folder = os.path.join(download_folder, "Downloads")
elif os.name == "nt":  # Windows
    download_folder = os.path.join(download_folder, "Downloads")
else:
    print("Unsupported operating system. Download folder not set.")

# Create the download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

# Download the video to the specified path
stream.download(output_path=download_folder)

print(f"Video '{title}' has been downloaded to {download_folder}")
