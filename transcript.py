import argparse
import youtube_transcript_api

def get_transcript(url):
    try:
        # From the URL, fetch the video ID
        video_id = url.split("v=")[1]

        # Fetch the transcript using the YouTube transcript api
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)

        # Extract the text from the transcript
        text = ""
        for line in transcript:
            text += line['text'] + '\n'

        return text
    except youtube_transcript_api.CouldNotRetrieveTranscript:
        print(f"Error: Could not retrieve transcript for video {video_id}")
        return None
    except IndexError:
        print("Error: Invalid URL")
        return None

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", help="the YouTube URL of the video")
args = parser.parse_args()

# Get the transcript
transcript = get_transcript(args.url)

# Write the transcript to the file
if transcript:
    with open("transcript.txt", "w") as f:
        f.write(transcript)
    print(f"Transcript for video {video_id} written to transcript.txt")
else:
    print("Transcript not written to file")
