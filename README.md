# YouTube Transcript Downloader

A Python script that utilizes the `youtube_transcript_api` library to fetch the transcript (captions) of a YouTube video and write it into a text file.

## Features

- Fetches publicly available transcripts for YouTube videos.
- Supports various YouTube URL formats (e.g., `watch?v=`, `youtu.be/`, `/embed/`).
- Attempts to handle URLs pasted directly into shells that might auto-escape special characters (like `?` becoming `\?`).
- Allows specifying a custom output file name.
- Outputs the transcript as plain text, with each segment typically on a new line.

## Prerequisites

1.  **Python 3:** Make sure you have Python 3 installed on your computer. You can check by running `python3 --version`.
2.  **`youtube_transcript_api` library:** This script depends on the `youtube_transcript_api` library.

## Installation

If you don't have the required library installed, open your command prompt or terminal and run:

```bash
pip3 install youtube_transcript_api
```

## Usage

Navigate to the directory where the transcript.py script is located using your command prompt or terminal.
Then, run the script using the following format:

python3 transcript.py <youtubeURL> [OPTIONS]

Where <youtubeURL> is the link to the YouTube video you want the transcript of.

## Options

- -o <filename> or --output <filename>: Specify a name for the output transcript file. If omitted, the transcript will be saved to transcript.txt by default.

The .txt file of this repository shows the transcript of [the following YouTube video](https://www.youtube.com/watch?v=zhWDdy_5v2w).
