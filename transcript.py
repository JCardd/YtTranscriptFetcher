import argparse
import sys  # Used for exiting with an error code

# Make sure the library name is correct (it's youtube_transcript_api)
from youtube_transcript_api import (
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)


def get_video_id(url):
    """
    Extracts the YouTube video ID from various URL formats.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: The extracted video ID, or None if it cannot be extracted.
    """
    video_id = None
    try:
        if "watch?v=" in url:
            # Handles URLs like: https://www.youtube.com/watch?v=VIDEO_ID&...
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            # Handles URLs like: https://youtu.be/VIDEO_ID?t=...
            video_id = url.split("youtu.be/")[1].split("?")[0]
        elif "/embed/" in url:
            # Handles URLs like: https://www.youtube.com/embed/VIDEO_ID
            video_id = url.split("/embed/")[1].split("?")[0]
        # Add more robust parsing or checks if needed
    except IndexError:
        # This can happen if the split operations fail unexpectedly
        print(f"Error: Could not parse video ID from URL: {url}")
        return None  # Explicitly return None on parsing failure

    # Basic check if the extracted ID looks plausible (alphanumeric, -, _)
    if video_id and all(c.isalnum() or c in ["-", "_"] for c in video_id):
        return video_id
    else:
        # Handle cases where splitting worked but didn't yield a valid ID format
        # or if no known pattern was matched
        if video_id:  # If split produced something invalid
            print(f"Warning: Extracted ID '{video_id}' seems invalid from URL: {url}")
        else:  # If no pattern matched
            print(f"Error: Could not recognize YouTube video ID pattern in URL: {url}")
        return None


def get_transcript(video_id, url):
    """
    Fetches the transcript for a given YouTube video ID.

    Args:
        video_id (str): The ID of the YouTube video.
        url (str): The original URL (used for error messages).

    Returns:
        str: The transcript text, with each line separated by a newline,
             or None if the transcript cannot be retrieved.
    """
    try:
        # Fetch the transcript using the YouTube transcript api
        # Returns a list of dictionaries [{'text': '...', 'start': ..., 'duration': ...}, ...]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Extract and format the text from the transcript list
        transcript_text = ""
        for line in transcript_list:
            # Append the text of each segment, followed by a newline
            transcript_text += line["text"] + "\n"

        # Remove trailing newline if present
        return transcript_text.strip()

    # Catch specific errors from the API for more informative messages
    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video ID {video_id} (URL: {url})")
        return None
    except NoTranscriptFound:
        print(
            f"Error: No transcript found for video ID {video_id} (URL: {url}). The video might not have captions or they aren't available in a retrievable format."
        )
        return None
    except CouldNotRetrieveTranscript as e:  # Catch other potential API errors
        print(
            f"Error: Could not retrieve transcript for video ID {video_id} (URL: {url}). Reason: {e}"
        )
        return None
    except Exception as e:  # Catch any other unexpected exceptions during API call
        print(
            f"An unexpected error occurred while fetching transcript for {video_id} (URL: {url}): {e}"
        )
        return None


def main():
    """
    Main function to parse arguments, fetch transcript, and write to file.
    """
    # --- Setup Argument Parser ---
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube video transcript and save it to transcript.txt."
    )
    # The URL is a required positional argument
    parser.add_argument(
        "url",
        help="The full YouTube URL of the video (e.g., 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="transcript.txt",
        help="Output filename (default: transcript.txt)",
    )

    # --- Parse Arguments ---
    args = parser.parse_args()
    youtube_url = args.url
    output_filename = args.output

    # --- Get Video ID ---
    print(f"Attempting to extract video ID from URL: {youtube_url}")
    video_id = get_video_id(youtube_url)

    if not video_id:
        # Error message already printed by get_video_id if it failed
        sys.exit(1)  # Exit with a non-zero code to indicate failure

    print(f"Extracted Video ID: {video_id}")

    # --- Get Transcript ---
    print(f"Fetching transcript for video ID: {video_id}...")
    transcript = get_transcript(video_id, youtube_url)  # Pass video_id and original url

    # --- Write Transcript to File ---
    if transcript:
        print(f"Transcript retrieved successfully. Writing to '{output_filename}'...")
        try:
            # Use 'w' mode (write) and specify utf-8 encoding for broader character support
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Transcript successfully written to {output_filename}")
        except IOError as e:
            # Handle potential file writing errors
            print(
                f"Error: Could not write transcript to file '{output_filename}'. Reason: {e}"
            )
            sys.exit(1)  # Exit with error
    else:
        # Error messages should have been printed by get_transcript()
        print("Failed to retrieve transcript. File not written.")
        sys.exit(1)  # Exit with error


# --- Script Entry Point ---
if __name__ == "__main__":
    # This ensures the main() function runs only when the script is executed directly
    main()
