import subprocess
import os
import json

def get_video_duration(input_file):
    """
    Retrieves the duration of the video using ffprobe.
    Args:
        input_file (str): Path to the input video file.
    Returns:
        float: Duration of the video in seconds.
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", input_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get video information: {result.stderr}")
    
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def reduce_video_size(input_file, output_file, target_size_mb):
    """
    Compresses a video file to a target size in MB.
    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to save the output compressed video file.
        target_size_mb (int): Target size for the compressed video in MB.
    """
    try:
        # Get the current file size in MB
        input_size_mb = os.path.getsize(input_file) / (1024 * 1024)

        # Get the video duration
        duration = get_video_duration(input_file)

        # Determine the target bitrate in kilobits per second (kbps)
        target_bitrate = (target_size_mb * 8192) / duration

        print(f"Original Size: {input_size_mb:.2f} MB")
        print(f"Target Size: {target_size_mb} MB")
        print(f"Target Bitrate: {target_bitrate:.2f} kbps")

        # Run ffmpeg to compress the video
        subprocess.run(
            [
                "ffmpeg", "-i", input_file, "-b:v", f"{int(target_bitrate)}k", "-b:a", "128k",
                "-c:v", "libx264", "-preset", "slow", "-crf", "24", output_file
            ],
            check=True
        )

        print(f"Compression finished. File saved as {output_file}")

    except RuntimeError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    input_video = "1.mp4"  # Change this to your video path
    output_video = "2.mp4"
    target_size = 180  # Target size in MB

    reduce_video_size(input_video, output_video, target_size)
