import argparse
import youtube_transcript_api

def get_transcript(url):
    # Extract the video id from the URL
    video_id = url.split("v=")[1]

    # Use the youtube_transcript_api library to fetch the transcript
    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
   
    # Extract the text from the transcript
    text = ""
    for line in transcript:
        text += line['text'] + '\n'

    return text

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", help="the YouTube URL of the video")
args = parser.parse_args()

# Fetch the transcript
transcript = get_transcript(args.url)

# Write the transcript to a file
with open("transcript.txt", "w") as f:
    f.write(transcript)
