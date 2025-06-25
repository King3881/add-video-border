# Video Resizer with Black Borders

This Python script resizes an MP4 video and adds black borders (approximately 5% top and bottom) to center the content while maximizing the video area.

## Features

*   Resizes video to fit within the original dimensions.
*   Adds black borders to the top and bottom (approximately 5% each).
*   Maximizes the video area while maintaining the original aspect ratio.
*   Uses OpenCV for video processing.
*   **Accepts input and output filenames as command-line arguments.**

*   NEW
*   add_vid_border_with_audio.py use ffmpeg to merge the original video audio into the bordered video
*   ffmpeg.exe included

## Prerequisites

*   Python 3.6 or higher
*   OpenCV (`opencv-python`)
*   NumPy (`numpy`)
*   ffmpeg (for audio included)

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

[Optional]
3. Install/Download ffmpeg exe (for add_vid_border_with_audio.py only)
4. Put ffmpeg.exe in the same directory with add_vid_border_with_audio.py

## Usage

1.  **Run the script with command-line arguments :**

    ```bash
    python add_vid_border.py input.mp4 output.mp4
    ```

    *   Replace `input.mp4` with the name of your input video file.
    *   Replace `output.mp4` with the desired name for the output video file.
    *   Default 5% border


    ```bash
    python add_vid_border.py input.mp4 output.mp4 --border 10
    ```

    * 10% border around the video
  

     ```bash
    python add_vid_border_with_audio.py input.mp4 output.mp4
    ```

    * add border and include audio


2.  **Alternatively, run the script without arguments:**

    ```bash
    python add_vid_border.py
    ```

    *   If you run the script without arguments, it will use the default input filename `input.mp4` and the default output filename `output.mp4`.  Make sure to rename your input video to `input.mp4` in this case.



## Customization

*   To adjust the border size, you'll need to modify the script's calculations (the `0.9` value controls the maximum video height).

## License

This project is licensed under the [MIT License](LICENSE).

## Author

[King3881](https://github.com/King3881)
