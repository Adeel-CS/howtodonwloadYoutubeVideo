import subprocess
import sys

# Function to install a package using pip
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install pytube if it's not already installed
try:
    from pytube import YouTube
except ImportError:
    print("pytube not found. Installing...")
    install_package("pytube")
    from pytube import YouTube

def download_youtube_video(url, output_path="."):
    try:
        # Create a YouTube object with the URL
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        stream = yt.streams.get_highest_resolution()
        
        # Download the video to the specified directory
        stream.download(output_path=output_path)
        
        print(f"Downloaded: {yt.title} to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example URL (you can replace this with any YouTube video URL)
    # url = input("Enter the YouTube video URL: ")
    url = "https://youtu.be/r0XJrdSXJuU?si=3jVrREz8pcgWht5Q"
    # output_path = input("Enter the directory to save the video (default is current directory): ")
    # output_path = r'D:\All_Adeels\University\EAD'  # Using raw string
    # If no output path is provided, use the current directory
    # if not output_path:
        # output_path = "."
    output_path = "."
    download_youtube_video(url, output_path)
