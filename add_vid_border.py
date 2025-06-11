import cv2
import numpy as np
import sys
import argparse
import os

def resize_video_with_black_borders(input_path, output_path, border_percentage=5):
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Video file not found: {input_path}")

    # Open the input video
    cap = cv2.VideoCapture(input_path)

    # Check if video opened successfully
    if not cap.isOpened():
        raise ValueError(f"Error: Could not open video file '{input_path}'. Check if file exists and is a valid video format.")

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Validate video dimensions
    if original_width <= 0 or original_height <= 0:
        cap.release()
        raise ValueError(f"Error: Invalid video dimensions ({original_width}x{original_height}). Video file may be corrupted or empty.")

    # Validate and fix FPS
    if fps <= 0:
        fps = 30  # Default fallback
        print("Warning: Could not detect FPS, using default 30 FPS")

    # Calculate new dimensions based on border percentage
    border_factor = (100 - border_percentage * 2) / 100  # Account for borders on both sides
    video_height = int(original_height * border_factor)

    # Calculate video width to fill as much horizontal space as possible
    # while maintaining aspect ratio
    original_aspect_ratio = original_width / original_height
    video_width = int(video_height * original_aspect_ratio)

    # If the calculated width exceeds available width, scale down proportionally
    max_video_width = int(original_width * border_factor)
    if video_width > max_video_width:
        video_width = max_video_width
        video_height = int(video_width / original_aspect_ratio)

    # Output dimensions (same as original)
    output_width = original_width
    output_height = original_height

    # Calculate positioning for centering
    x_offset = (output_width - video_width) // 2
    y_offset = (output_height - video_height) // 2

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))

    # Check if video writer opened successfully
    if not out.isOpened():
        cap.release()
        raise ValueError(f"Error: Could not create output video file '{output_path}'. Check if the path is valid and writable.")

    print(f"Border percentage: {border_percentage}%")
    print(f"Original: {original_width}x{original_height}")
    print(f"Resized video: {video_width}x{video_height}")
    print(f"Position: ({x_offset}, {y_offset})")
    print(f"Top/Bottom borders: ~{y_offset}px each ({y_offset/original_height*100:.1f}%)")
    print(f"Left/Right borders: ~{x_offset}px each ({x_offset/original_width*100:.1f}%)")
    print(f"FPS: {fps}")

    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame
            resized_frame = cv2.resize(frame, (video_width, video_height))

            # Create black canvas
            canvas = np.zeros((output_height, output_width, 3), dtype=np.uint8)

            # Place resized frame in center
            canvas[y_offset:y_offset+video_height, x_offset:x_offset+video_width] = resized_frame

            # Write frame
            out.write(canvas)
            frame_count += 1

            if frame_count % 30 == 0:  # Progress indicator
                progress = (frame_count / total_frames * 100) if total_frames > 0 else 0
                print(f"Processed {frame_count} frames... ({progress:.1f}%)")

    except Exception as e:
        print(f"Error during video processing: {e}")
        raise

    finally:
        # Release everything
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    print(f"Video processing complete! Output saved to: {output_path}")
    print(f"Total frames processed: {frame_count}")

# Usage with command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add black borders to video')
    parser.add_argument('input_video', help='Input video file path')
    parser.add_argument('output_video', help='Output video file path')
    parser.add_argument('-b', '--border', type=float, default=5.0, 
                        help='Border percentage (default: 5.0)')

    args = parser.parse_args()

    # Validate border percentage
    if args.border < 0 or args.border >= 50:
        print("Error: Border percentage must be between 0 and 50")
        sys.exit(1)

    try:
        resize_video_with_black_borders(args.input_video, args.output_video, args.border)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
