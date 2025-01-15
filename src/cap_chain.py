# cap_chain.py
from typing import Dict
from PIL import Image

class CaptioningChain:
    """Enhanced chain for image captioning using dual Gemini Vision models"""
    
    def __init__(self, model1, model2):
        self.primary_model = model1
        self.secondary_model = model2
        self._init_prompts()

    def _init_prompts(self):
        """Initialize detailed prompts for each component"""
        self.prompts = {
            "base_description": """
            Provide a clear, factual description of the key elements visible in this image.
            Focus on the main subjects, actions, and setting in 2-3 sentences.
            """,
            "detailed_analysis": """
            Please provide a detailed analysis of this image with the following sections:

            1. Subject Analysis (People, Objects, Actions):
            - Describe all visible people, their appearance, Ethnicity, skin color, clothing, and actions
            - Detail important objects, their characteristics and placement
            - Note any significant interactions or movements

            2. Environment and Setting:
            - Describe the location and surroundings
            - Note lighting conditions and atmosphere
            - Identify any notable background elements

            3. Technical Aspects:
            - Camera angle and shot type
            - Lighting quality and direction
            - Composition and framing
            - Any notable photographic techniques used

            Be objective and focus only on visible elements.
            """,
            "final_summary": """
            Create a comprehensive yet concise summary (2-3 sentences) that captures:
            - The key visual elements and their relationships
            - The overall mood and impact of the image
            - Any notable or unique aspects
            """
        }

    def _generate_with_context(self, image: Image.Image, prompt: str, 
                             context: Dict[str, str] = None) -> str:
        """Generate content with context awareness"""
        # Construct the complete prompt
        if context:
            enhanced_prompt = f"""
            Previous Analysis Context:
            {str(context)}
            
            New Analysis Task:
            {prompt}
            """
        else:
            enhanced_prompt = prompt
            
        # Alternate between models for load balancing
        model = self.primary_model if len(context or {}) % 2 == 0 else self.secondary_model
        
        try:
            response = model.generate_content([enhanced_prompt, image])
            return response.text
        except Exception as e:
            raise Exception(f"Image analysis failed: {str(e)}")

    def __call__(self, inputs: Dict) -> Dict[str, str]:
        """Execute the chain with enhanced context handling"""
        image = inputs["image"]
        results = {}
        context = {}
        
        # Generate components sequentially with context
        for key, prompt in self.prompts.items():
            results[key] = self._generate_with_context(image, prompt, context)
            context[key] = results[key]
        
        return results
