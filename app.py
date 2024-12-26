from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import base64
import google.generativeai as genai
import logging
from PIL import Image
import io
import re

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
GEMINI_API_KEY = "AIzaSyCHIGVlOgUmiPy-_1UFjqlXUWkfrvDWc1k"
HF_API_TOKEN = "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"

class AIGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        self.hf_model = "stabilityai/stable-diffusion-2-1"
    
    def format_text_content(self, text: str) -> str:
        """Format text content for better readability without asterisks"""
        # Remove asterisks
        text = re.sub(r'\*+', '', text)
        
        # Split into sections and clean up
        sections = []
        current_section = []
        
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line:
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            else:
                # Remove any remaining special characters or markdown
                line = re.sub(r'[#_~]', '', line)
                current_section.append(line)
        
        if current_section:
            sections.append('\n'.join(current_section))
        
        return '\n\n'.join(sections)

    def generate_text(self, prompt: str) -> str:
        try:
            enhanced_prompt = f"""
            Provide information about {prompt}. Include:
            1. A clear introduction
            2. Key characteristics and features
            3. Interesting and unique aspects
            4. Practical applications or relevant details
            
            Please provide the information in clear paragraphs without using any special characters, asterisks, or markdown formatting.
            Keep the tone professional and informative.
            """
            
            response = self.gemini_model.generate_content(enhanced_prompt)
            if not response.text:
                raise ValueError("No text generated from the model")
                
            formatted_response = self.format_text_content(response.text)
            return formatted_response
            
        except Exception as e:
            logger.error(f"Text generation error: {str(e)}")
            raise

    def generate_image(self, prompt: str) -> bytes:
        try:
            # Enhanced prompt to generate more accurate and relevant images
            enhanced_prompt = (
                f"A highly detailed, photorealistic visualization of {prompt}, "
                "professional quality, sharp focus, perfect lighting, "
                "4k resolution, modern style, trending on artstation"
            )
            
            api_url = f"https://api-inference.huggingface.co/models/{self.hf_model}"
            headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
            
            # Add parameters to improve image generation
            payload = {
                "inputs": enhanced_prompt,
                "parameters": {
                    "guidance_scale": 7.5,  # Higher value for more prompt-focused images
                    "num_inference_steps": 50  # More steps for better quality
                }
            }
            
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                raise ValueError(f"Image generation failed: {response.text}")
                
            return response.content
            
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            raise

    def generate_both(self, prompt: str):
        try:
            text = self.generate_text(prompt)
            image = self.generate_image(prompt)
            return text, image
        except Exception as e:
            logger.error(f"Combined generation error: {str(e)}")
            raise

# Initialize generator
generator = AIGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/placeholder/<int:width>/<int:height>')
def placeholder_image(width: int, height: int):
    """Generate a placeholder image with specified dimensions"""
    try:
        # Create a simple gradient placeholder
        img = Image.new('RGB', (width, height), color='#141414')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return send_file(img_byte_arr, mimetype='image/png')
    except Exception as e:
        logger.error(f"Placeholder generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate placeholder'}), 500

@app.route('/generate-text', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
        
        text = generator.generate_text(data['prompt'])
        return jsonify({'text': text})
    except Exception as e:
        logger.error(f"Text generation endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400

        image_bytes = generator.generate_image(data['prompt'])
        if not image_bytes:
            return jsonify({'error': 'Image generation failed'}), 500

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return jsonify({'image_url': f"data:image/png;base64,{image_base64}"})
    except Exception as e:
        logger.error(f"Image generation endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-both', methods=['POST'])
def generate_both():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400

        text, image_bytes = generator.generate_both(data['prompt'])
        response = {'text': text}
        
        if image_bytes:
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            response['image_url'] = f"data:image/png;base64,{image_base64}"

        return jsonify(response)
    except Exception as e:
        logger.error(f"Combined generation endpoint error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)