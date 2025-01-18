import os
import subprocess
from termcolor import colored
import whisper
from pathlib import Path
import torch
import warnings
from contextlib import contextmanager
import time
import shutil

# Constants
DEFAULT_INPUT_DIR = "input_videos"
OUTPUT_DIR = "output_audio"
TRANSCRIPTS_DIR = "transcripts"
WHISPER_MODEL = "base"  # Can be tiny, base, small, medium, or large

@contextmanager
def suppress_warnings():
    """Context manager to temporarily suppress warnings."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        yield

def load_whisper_model():
    """Load Whisper model with proper warning handling."""
    try:
        with suppress_warnings():
            model = whisper.load_model(
                WHISPER_MODEL,
                device="cpu"  # Explicitly use CPU to avoid FP16 warning
            )
        return model
    except Exception as e:
        raise Exception(f"Error loading Whisper model: {str(e)}")

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    try:
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            raise Exception("FFmpeg not found. Please install FFmpeg and make sure it's in your system PATH.")
        
        # Test ffmpeg version
        process = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if process.returncode != 0:
            raise Exception("FFmpeg installation appears to be corrupted or incomplete.")
            
        return True
    except Exception as e:
        print(colored(f"FFmpeg Error: {str(e)}", "red"))
        raise

def setup_directories():
    """Create necessary directories if they don't exist."""
    try:
        for dir_name in [DEFAULT_INPUT_DIR, OUTPUT_DIR, TRANSCRIPTS_DIR]:
            os.makedirs(dir_name, exist_ok=True)
            # Check write permissions
            test_file = os.path.join(dir_name, ".test")
            try:
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)
            except Exception as e:
                raise Exception(f"No write permission in directory: {dir_name}")
                
        print(colored("✓ Directories setup complete", "green"))
    except Exception as e:
        print(colored(f"Error creating/accessing directories: {str(e)}", "red"))
        raise

def convert_video_to_audio(video_path):
    """Convert MP4 video to MP3 audio using ffmpeg."""
    try:
        if not os.path.exists(video_path):
            raise Exception(f"Video file not found: {video_path}")
            
        if not os.path.isfile(video_path):
            raise Exception(f"Not a valid file: {video_path}")
            
        # Check if it's actually an MP4 file
        if not video_path.lower().endswith('.mp4'):
            raise Exception(f"Not an MP4 file: {video_path}")
            
        print(colored(f"Converting {video_path} to audio...", "yellow"))
        output_path = os.path.join(OUTPUT_DIR, os.path.splitext(os.path.basename(video_path))[0] + ".mp3")
        
        # Clean up the output path if it exists
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception:
                pass

        # Build ffmpeg command
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",  # Disable video
            "-acodec", "libmp3lame",
            "-ab", "192k",
            "-ar", "44100",
            "-y",  # Overwrite output file if exists
            output_path
        ]
        
        # Start the process
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if process.returncode == 0:
            if not os.path.exists(output_path):
                raise Exception("FFmpeg completed but output file not found")
                
            print(colored(f"✓ Audio conversion successful: {output_path}", "green"))
            return output_path
        else:
            error_msg = process.stderr.strip() if process.stderr else "Unknown FFmpeg error"
            raise Exception(f"FFmpeg error: {error_msg}")
            
    except Exception as e:
        # Clean up any partial output
        if 'output_path' in locals() and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception:
                pass
        print(colored(f"Error converting video to audio: {str(e)}", "red"))
        raise

def transcribe_audio(audio_path):
    """Transcribe audio file using Whisper."""
    try:
        if not os.path.exists(audio_path):
            raise Exception(f"Audio file not found: {audio_path}")
            
        print(colored(f"Transcribing {audio_path}...", "yellow"))
        
        # Load model and transcribe
        model = load_whisper_model()
        with suppress_warnings():
            result = model.transcribe(audio_path)
        
        if not result or "text" not in result:
            raise Exception("Transcription produced no output")
        
        # Save transcript
        transcript_path = os.path.join(
            TRANSCRIPTS_DIR,
            os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
        )
        
        try:
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
        except Exception as e:
            raise Exception(f"Error saving transcript: {str(e)}")
            
        print(colored(f"✓ Transcription saved to: {transcript_path}", "green"))
        return transcript_path
        
    except Exception as e:
        print(colored(f"Error transcribing audio: {str(e)}", "red"))
        raise
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

def process_video(video_path):
    """Process a single video file."""
    try:
        audio_path = convert_video_to_audio(video_path)
        transcript_path = transcribe_audio(audio_path)
        return transcript_path
    except Exception as e:
        print(colored(f"Error processing video {video_path}: {str(e)}", "red"))
        raise

def main():
    """Main function to process all videos in the input directory."""
    try:
        # Check ffmpeg installation first
        check_ffmpeg()
        
        setup_directories()
        
        # Get all MP4 files from input directory
        video_files = list(Path(DEFAULT_INPUT_DIR).glob("*.mp4"))
        
        if not video_files:
            print(colored("No MP4 files found in the input directory!", "yellow"))
            return
            
        print(colored(f"Found {len(video_files)} video files to process", "cyan"))
        
        for video_file in video_files:
            print(colored(f"\nProcessing: {video_file}", "cyan"))
            process_video(str(video_file))
            
        print(colored("\n✓ All videos processed successfully!", "green"))
        
    except Exception as e:
        print(colored(f"Error in main process: {str(e)}", "red"))
        raise

if __name__ == "__main__":
    main() 