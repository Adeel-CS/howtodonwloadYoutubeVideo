import subprocess
import sys
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def install_package(package):
    """
    Install a Python package using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Installed {package} successfully!")
    except subprocess.CalledProcessError:
        print(f"Error installing {package}. Please check your internet connection or try again later.")

def download_youtube_transcript(url, languages=['en']):
    try:
        # Check if pytube and youtube-transcript-api are already imported
        try:
            from pytube import YouTube
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            print("pytube or youtube-transcript-api not found. Installing...")
            install_package("pytube")
            install_package("youtube-transcript-api")
            from pytube import YouTube
            from youtube_transcript_api import YouTubeTranscriptApi

        # Create a YouTube object with the URL
        yt = YouTube(url)
        video_id = yt.video_id  # Get the video ID

        # Check available languages
        available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = [transcript.language_code for transcript in available_transcripts]

        print(f"Available languages for this video: {available_languages}")

        transcripts = {}
        for lang in languages:
            if lang in available_languages:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                transcripts[lang] = transcript
            else:
                print(f"No transcript available for language: {lang}")

        # Save transcripts to separate files
        for lang, transcript in transcripts.items():
            filename = f"{yt.title}_{lang}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                for entry in transcript:
                    file.write(f"{entry['text']}\n")
            print(f"Transcript ({lang}) saved as {filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example URL (you can replace this with any YouTube video URL)
    url = "https://youtu.be/r0XJrdSXJuU?si=3jVrREz8pcgWht5Q"
    languages = ['en', 'hi', 'ur']  # English, Hindi, Urdu
    download_youtube_transcript(url, languages)
