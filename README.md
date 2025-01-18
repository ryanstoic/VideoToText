# Video to Text Converter 🎥 ➡️ 📝

Transform your videos into text effortlessly! This sleek web app uses OpenAI's Whisper to turn your MP4s into accurate transcripts with real-time progress tracking and a beautiful dark-mode interface.

A modern web application that converts video files to text using OpenAI's Whisper model. Built with FastAPI, WebSockets, and a clean dark-mode UI.

## Features

- Convert MP4 videos to text transcripts
- Real-time progress updates via WebSocket
- Modern dark-mode UI with DaisyUI and Tailwind CSS
- Batch processing of multiple videos
- Clean and informative error handling
- Progress tracking for each file

## Requirements

- Python 3.9+
- FFmpeg installed and in system PATH
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ryanstoic/VideoToText.git
cd VideoToText
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure FFmpeg is installed and accessible from PATH:
- Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

## Usage

1. Start the server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

3. Enter the directory path containing your MP4 files
4. Click "Process Videos" to start the conversion
5. Monitor progress in real-time
6. Find transcripts in the `transcripts` directory

## Project Structure

```
VideoToText/
├── main.py              # FastAPI server and WebSocket handling
├── video_to_text.py     # Core video processing and transcription logic
├── index.html           # Frontend UI
├── static/             
│   └── styles.css       # Additional styles
├── input_videos/        # Default directory for input videos
├── output_audio/        # Temporary audio files
└── transcripts/         # Output transcripts
```

## Dependencies

- FastAPI - Web framework
- Whisper - OpenAI's speech recognition model
- FFmpeg - Audio/video processing
- DaisyUI - UI components
- Tailwind CSS - Styling
- anime.js - Animations

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid directories
- Unsupported file formats
- FFmpeg processing errors
- Transcription failures
- File system permissions
- Network disconnections

## Notes

- Supports MP4 video files
- Transcripts are saved as UTF-8 text files
- Audio files are temporarily stored in output_audio/
- Progress updates are real-time via WebSocket
- Uses CPU for transcription by default

## License

MIT License

Copyright (c) 2024 ryanstoic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 