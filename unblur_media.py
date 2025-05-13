"""
Simple and powerful script to sharpen ("unblur") an image or video using Python and OpenCV.

Usage:
    python unblur_media.py input_path output_path [sharpness_level]

Arguments:
    input_path       Path to the input image or video file.
    output_path      Path to save the sharpened output file.
    sharpness_level  (Optional) Integer controlling sharpening intensity (1-10), default is 3.

Requirements:
    Install OpenCV via pip:
        pip install opencv-python

This script automatically detects if the input file is an image or a video.
For videos, the output will be saved in the same format as input.
"""

import sys
import cv2
import numpy as np
import os

def is_image_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif']

def is_video_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.mpeg']

def sharpen_image(input_path, output_path, sharpness_level):
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Cannot read image file {input_path}")
        return False

    # Define sharpening kernel
    # Increasing sharpness_level increases the intensity of sharpening
    level = np.clip(sharpness_level, 1, 10)
    kernel = np.array([[0, -1, 0],
                       [-1, 5 + level, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(output_path, sharpened)
    print(f"Sharpened image saved to {output_path}")
    return True

def sharpen_video(input_path, output_path, sharpness_level):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {input_path}")
        return False

    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        print("Warning: Failed to open VideoWriter with input codec, trying default 'mp4v' codec.")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            print("Error: Cannot open video writer")
            cap.release()
            return False

    level = np.clip(sharpness_level, 1, 10)
    kernel = np.array([[0, -1, 0],
                       [-1, 5 + level, -1],
                       [0, -1, 0]])

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        sharpened_frame = cv2.filter2D(frame, -1, kernel)
        out.write(sharpened_frame)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames...", end='\r')

    cap.release()
    out.release()
    print(f"\nSharpened video saved to {output_path}")
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python unblur_media.py input_path output_path [sharpness_level]")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    sharpness_level = 3  # default sharpness intensity
    if len(sys.argv) >= 4:
        try:
            sharpness_level = int(sys.argv[3])
            if sharpness_level < 1 or sharpness_level > 10:
                print("Sharpness level must be between 1 and 10. Using default 3.")
                sharpness_level = 3
        except ValueError:
            print("Invalid sharpness_level value, must be an integer. Using default 3.")

    if not os.path.isfile(input_path):
        print(f"Error: input file {input_path} does not exist.")
        return

    if is_image_file(input_path):
        sharpen_image(input_path, output_path, sharpness_level)
    elif is_video_file(input_path):
        sharpen_video(input_path, output_path, sharpness_level)
    else:
        print("Error: input file type not recognized as image or video.")

if __name__ == "__main__":
    main()


