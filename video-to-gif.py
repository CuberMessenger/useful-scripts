import os
import argparse
from moviepy.editor import VideoFileClip


def video_to_gif(video_path, fps):
    # Extract the directory and base name for the output
    base, ext = os.path.splitext(video_path)
    gif_path = f"{base}.gif"

    # Load the video file
    clip = VideoFileClip(video_path).resize(0.5)

    # Write the GIF
    clip.write_gif(gif_path, fps=fps, program='ffmpeg', opt='optimizeplus')  # Using ffmpeg for better optimization
    clip.close()

    print(f"Converted {video_path} to {gif_path} at {fps} fps")


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Convert video to GIF")
    parser.add_argument("--path", type=str, help="Path to the video file")
    parser.add_argument(
        "--fps",
        type=int,
        default=8,
        help="Frames per second for the GIF (default: 8)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Convert video to GIF with specified fps
    video_to_gif(args.path, args.fps)


if __name__ == "__main__":
    main()
