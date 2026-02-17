# VAC - Video Audio Converter
VAC is a desktop application designed to download and convert media from YouTube, Spotify, and SoundCloud. It provides a unified interface for managing downloads, converting formats, and organizing media history.

## Features
Universal Downloader: Supports downloading content from YouTube (Video & Audio), Spotify (Audio), and SoundCloud (Audio).

Smart Format Switching: Automatically detects audio-only platforms (Spotify, SoundCloud) and locks the download format to MP3 to prevent errors.

High-Quality Audio: Forces 320kbps bitrate for audio downloads and automatically searches for "Official Audio" to avoid music video sound effects.

Drag-and-Drop Integration: Drag downloaded files directly from the application's history table into any Windows folder or desktop.

Download History: Maintains a persistent log of all downloads, including file size, date, and storage location.

Clean File Management: Automatically filters out temporary build files (like .opus or .part), ensuring only the final converted files appear in the history.

Privacy Handling: Includes error handling and prompts for private Spotify playlists.

Portable: Runs as a standalone executable with no installation required.

## Requirements
To ensure the application functions correctly, the following requirements must be met:

Operating System: Windows 10 or Windows 11.

Spotify Desktop Application: For Spotify downloads to work reliably, it is highly recommended to have the Spotify Desktop app installed and to be logged in with an active account.

FFmpeg: The application requires FFmpeg for media conversion. If using the pre-compiled executable, FFmpeg is bundled internally. If running from source, FFmpeg must be added to your system PATH.

Internet Connection: An active connection is required for all downloads.

## Usage
Paste Link: Copy a link from YouTube, Spotify, or SoundCloud and paste it into the input field.

Select Format: Choose between Video (MP4) or Audio (MP3)

Download: Click the "Start Download" button. The console will display the progress.

Manage Files: Once finished, the file will appear in the "History" tab. You can play the file, open its folder, or drag and drop the entry to move the file elsewhere.

## Building from Source
If you wish to compile the application yourself, use the following PyInstaller command to ensure all dependencies and drag-and-drop features function correctly:
```
pyinstaller --noconsole --onefile --name "VAC" --icon "images/vac-logo.ico" --add-data "fonts;fonts" --add-binary "ffmpeg;ffmpeg" --collect-all "spotdl" --collect-all "pykakasi" --collect-all "ytmusicapi" --collect-all "rich" "main.py"
```

## Disclaimer
This tool is intended for personal archiving and educational purposes only. Please respect copyright laws and the terms of service of the respective platforms when downloading content.