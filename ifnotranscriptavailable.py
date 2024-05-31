import subprocess
import sys
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def install_package(package):
    """
    Install a Python package using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Installed {package} successfully!")
    except subprocess.CalledProcessError:
        print(f"Error installing {package}. Please check your internet connection or try again later.")

def download_audio(yt):
    """
    Download the audio of the YouTube video.
    """
    try:
        # Select the audio stream with the highest quality
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download(filename=f"{yt.title}.mp3")
            print(f"Audio downloaded as {yt.title}.mp3")
        else:
            print("No audio stream available.")
    except Exception as e:
        print(f"Error downloading audio: {e}")

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
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                    transcripts[lang] = transcript
                except (NoTranscriptFound, TranscriptsDisabled):
                    print(f"No transcript found for language: {lang}")
            else:
                print(f"No transcript available for language: {lang}")

        # If any of the specified languages is missing, download the audio
        if any(lang not in transcripts for lang in languages):
            print("Transcript not available in one or more specified languages. Downloading audio...")
            download_audio(yt)
        else:
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
