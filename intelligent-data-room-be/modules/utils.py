import base64
import os

def image_to_base64(image_path: str) -> str:
    """Converts an image file to a base64 string."""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error converting image to base64: {e}")
    return None
