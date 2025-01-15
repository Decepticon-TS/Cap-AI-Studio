from PIL import Image
import requests
from io import BytesIO
import base64

class ImageProcessor:
    @staticmethod
    def load_image_from_url(url: str) -> Image.Image:
        """Load an image from a URL"""
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    @staticmethod
    def load_image_from_file(file) -> Image.Image:
        """Load an image from a file upload"""
        return Image.open(file)

    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
