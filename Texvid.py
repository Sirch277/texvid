from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from flask import Flask, request, send_file
import io

app = Flask(__name__)

def create_image_from_text(text, font_path, font_size, image_size):
    # Create a new image with the specified size and background color.
    image = Image.new("RGB", image_size, (255, 255, 255))

    # Load the font and create a text drawing object.
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(image)

    # Determine the size of the text and the position to draw it.
    text_size = draw.textsize(text, font=font)
    text_x = (image_size[0] - text_size[0]) / 2
    text_y = (image_size[1] - text_size[1]) / 2

    # Draw the text on the image.
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    return image

def create_video_from_frames(frames, output_path, fps):
    # Get the size of the first frame.
    frame_size = frames[0].shape[:2]

    # Initialize the video writer.
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    # Write each frame to the video writer.
    for frame in frames:
        writer.write(frame)

    # Release the video writer.
    writer.release()

@app.route("/text-to-video", methods=["POST"])
def text_to_video():
    # Get the input text from the request.
    text = request.form["text"]

    # Create the image frames from the text.
    frames = []
    for i in range(10):
        frame = create_image_from_text(text, "arial.ttf", 24, (640, 480))
        frames.append(np.array(frame))

    # Create the video from the image frames.
    output_path = "output.mp4"
    create_video_from_frames(frames, output_path, 30)

    # Return the video file to the client.
    video_file = open(output_path, "rb").read()
    return send_file(
        io.BytesIO(video_file),
        mimetype="video/mp4",
        as_attachment=True,
        attachment_filename=output_path
    )
