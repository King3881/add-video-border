import cv2
import numpy as np
import sys

def resize_video_with_black_borders(input_path, output_path):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate new dimensions
    # 90% of height for video content (5% top + 90% video + 5% bottom)
    video_height = int(original_height * 0.9)
    
    # Calculate video width to fill as much horizontal space as possible
    # while maintaining aspect ratio
    original_aspect_ratio = original_width / original_height
    video_width = int(video_height * original_aspect_ratio)
    
    # If the calculated width exceeds original width, scale down proportionally
    if video_width > original_width:
        video_width = original_width
        video_height = int(video_width / original_aspect_ratio)
    
    # Output dimensions (same as original)
    output_width = original_width
    output_height = original_height
    
    # Calculate positioning for centering
    x_offset = (output_width - video_width) // 2
    y_offset = (output_height - video_height) // 2  # Center vertically
    
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))
    
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
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_video> <output_video>")
        print("Example: python script.py ShortTest.mp4 output.mp4")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2]
    
    resize_video_with_black_borders(input_video, output_video)