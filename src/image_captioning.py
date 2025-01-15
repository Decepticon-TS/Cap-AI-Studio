from typing import Dict
import google.generativeai as genai

from cap_chain import CaptioningChain
from img_pro import ImageProcessor


class ImageCaptioningSystem:
    def __init__(self, gemini_key1: str, gemini_key2: str):
        """Initialize the system with two separate Gemini Vision models"""
        try:
            # Initialize first Gemini configuration and model
            genai.configure(api_key=gemini_key1)
            self.model1 = genai.GenerativeModel('gemini-1.5-flash')
            
            # Store the second key for switching configurations
            self.key2 = gemini_key2
            # Initialize second model (will switch configurations as needed)
            genai.configure(api_key=gemini_key2)
            self.model2 = genai.GenerativeModel('gemini-1.5-flash')
            
            # Reset to first key as default
            genai.configure(api_key=gemini_key1)
            
            # Initialize components
            self.chain = CaptioningChain(self.model1, self.model2)
            self.image_processor = ImageProcessor()
            
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini models: {str(e)}")

    def process_image(self, image_input) -> Dict[str, str]:
        """Process image from either URL or file with enhanced error handling"""
        try:
            # Load and process image
            if isinstance(image_input, str) and image_input.startswith(('http://', 'https://')):
                image = self.image_processor.load_image_from_url(image_input)
            else:
                image = self.image_processor.load_image_from_file(image_input)
            
            # Generate analysis components
            components = self.chain({"image": image})
            return components
            
        except Exception as e:
            raise Exception(f"Image processing failed: {str(e)}")
