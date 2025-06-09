# Video Resizer with Black Borders

This Python script resizes an MP4 video and adds black borders (approximately 5% top and bottom) to center the content while maximizing the video area.

## Features

*   Resizes video to fit within the original dimensions.
*   Adds black borders to the top and bottom (approximately 5% each).
*   Maximizes the video area while maintaining the original aspect ratio.
*   Uses OpenCV for video processing.

## Prerequisites

*   Python 3.6 or higher
*   OpenCV (`opencv-python`)
*   NumPy (`numpy`)

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/King3881/add-video-border.git
    cd add-video-border
    ```

2.  Install the required Python packages:

    ```bash
    pip install opencv-python numpy
    ```

## Usage

1.  **Prepare your input video:** Rename your input video file to `input.mp4` and place it in the same directory as the `add_vid_border.py` script.

2.  **Run the script:**

    ```bash
    python add_vid_border.py
    ```

3.  The processed video will be saved as `output.mp4` in the same directory.

## Customization

*   To change the input and output filenames, modify the `input_video` and `output_video` variables in the `add_vid_border.py` script.
*   To adjust the border size, you'll need to modify the script's calculations (the `0.9` value controls the maximum video height).

## License

This project is licensed under the [MIT License](LICENSE).

## Author

[King3881](https://github.com/King3881)
