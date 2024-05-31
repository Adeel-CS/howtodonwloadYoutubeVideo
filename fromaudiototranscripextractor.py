import subprocess
import sys
import os
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from google.cloud import speech
from pydub import AudioSegment

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
            audio_file = audio_stream.download(filename=f"{yt.title}.mp4")
            print(f"Audio downloaded as {yt.title}.mp4")
            return audio_file
        else:
            print("No audio stream available.")
            return None
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def transcribe_audio(audio_file_path):
    """
    Transcribe audio using Google Cloud Speech-to-Text.
    """
    try:
        # Convert audio to wav format if necessary
        if not audio_file_path.endswith('.wav'):
            audio = AudioSegment.from_file(audio_file_path)
            audio_file_path = audio_file_path.replace(".mp4", ".wav")
            audio.export(audio_file_path, format="wav")

        client = speech.SpeechClient()
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",  # Adjust this based on your needs
        )

        response = client.recognize(config=config, audio=audio)

        # Save transcription to a text file
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript + "\n"

        transcription_file = audio_file_path.replace(".wav", "_transcription.txt")
        with open(transcription_file, "w", encoding="utf-8") as file:
            file.write(transcription)
        print(f"Transcription saved as {transcription_file}")

    except Exception as e:
        print(f"Error transcribing audio: {e}")

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

        # If any of the specified languages is missing, download the audio and transcribe
        if any(lang not in transcripts for lang in languages):
            print("Transcript not available in one or more specified languages. Downloading audio...")
            audio_file_path = download_audio(yt)
            if audio_file_path:
                transcribe_audio(audio_file_path)
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
