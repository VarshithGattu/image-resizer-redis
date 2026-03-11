import os
from PIL import Image
from rq import get_current_job
import logging

# Setup basic logging
logger = logging.getLogger(__name__)

def resize_image(input_path, resize_to_width, resize_to_height):
    """
    Resizes an image using PIL (Pillow).
    """

    # Get the job ID for logging
    job = get_current_job()
    job_id = job.id if job else "unknown_id"

    print(f"--- Processing Job {job_id} ---")

    # Generate output path
    directory, filename = os.path.split(input_path)
    output_filename = f"resized_{job_id}_{resize_to_width}x{resize_to_height}.jpg"
    output_path = os.path.join(directory, output_filename)

    try:
        # Open the image
        with Image.open(input_path) as img:

            # Convert to RGB if needed (for PNG → JPG conversion)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize image
            resized_img = img.resize((resize_to_width, resize_to_height))

            # Save resized image
            resized_img.save(output_path, "JPEG")

        print(f"--- SUCCESS: Image saved to {output_path} ---")

        return output_path

    except FileNotFoundError:
        error_msg = f"Original file not found at {input_path}"
        print(error_msg)
        raise

    except Exception as e:
        error_msg = f"Unexpected error during resize: {e}"
        print(error_msg)
        raise