import cv2
import numpy as np
import sys
import argparse

def resize_video_with_black_borders(input_path, output_path, border_percentage=5):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
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
    
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))
    
    print(f"Border percentage: {border_percentage}%")
    print(f"Original: {original_width}x{original_height}")
    print(f"Resized video: {video_width}x{video_height}")
    print(f"Position: ({x_offset}, {y_offset})")
    print(f"Top/Bottom borders: ~{y_offset}px each ({y_offset/original_height*100:.1f}%)")
    print(f"Left/Right borders: ~{x_offset}px each ({x_offset/original_width*100:.1f}%)")
    
    frame_count = 0
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
            print(f"Processed {frame_count} frames...")
    
    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"Video processing complete! Output saved to: {output_path}")

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
    
    resize_video_with_black_borders(args.input_video, args.output_video, args.border)