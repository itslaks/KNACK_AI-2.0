# KNACK_AI 2.0 🚀

KNACK_AI 2.0 is an AI-powered application that combines text and image generation capabilities using advanced AI models. This application provides endpoints for generating text, images, or both simultaneously through a user-friendly Flask API. The project also includes a web interface for rendering the generated content.

## Table of Contents 📑

- Features
- Technologies Used
- Prerequisites
- Setup and Installation
- API Endpoints
  - Generate Text
  - Generate Image
  - Generate Both
  - Placeholder Image
- Usage Instructions
- Logging
- Project Structure
- Contributing
- License

---

## Features ✨

1. Text Generation: Generates professional and informative content based on user prompts using the Gemini AI model.
2. Image Generation: Creates high-quality, photorealistic images from prompts using the Stable Diffusion model.
3. Combined Generation: Produces both text and image based on a single prompt.
4. Placeholder Images: Generates placeholder images with specified dimensions.
5. API Integration: Exposes RESTful API endpoints for seamless integration.
6. Web Interface: Renders generated content through an HTML interface.

---

## Technologies Used 🛠️

- Backend Framework: Flask
- Frontend: HTML (via Flask templates)
- Image Processing: PIL (Python Imaging Library)
- API Requests: `requests`
- AI Models:
  - Text: Google Gemini Pro (via `google.generativeai`)
  - Images: Stability AI's Stable Diffusion
- Logging: Python logging module
- Cross-Origin Resource Sharing: Flask-CORS

---

## Prerequisites ✅

- Python 3.8 or higher
- An active Google Gemini Pro API Key
- An active Hugging Face API Token

---

## Setup and Installation 🔧

1. Clone the repository:
   ```bash
   git clone https://github.com/itslaks/KNACK_AI_2.0.git
   cd KNACK_AI_2.0
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Replace the placeholders in `GEMINI_API_KEY` and `HF_API_TOKEN` in `app.py` with your actual API keys.

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application at `http://127.0.0.1:5000/` in your browser.

---

## API Endpoints 🔗

### Generate Text 📝
- Endpoint: `/generate-text`
- Method: POST
- Request Body:
  ```json
  {
    "prompt": "Your text prompt here"
  }
  ```
- Response:
  ```json
  {
    "text": "Generated text content."
  }
  ```

### Generate Image 🖼️
- Endpoint: `/generate-image`
- Method: POST
- Request Body:
  ```json
  {
    "prompt": "Your image prompt here"
  }
  ```
- Response:
  ```json
  {
    "image_url": "data:image/png;base64,..."
  }
  ```

### Generate Both 🌟
- Endpoint: `/generate-both`
- Method: POST
- Request Body:
  ```json
  {
    "prompt": "Your combined prompt here"
  }
  ```
- Response:
  ```json
  {
    "text": "Generated text content.",
    "image_url": "data:image/png;base64,..."
  }
  ```

### Placeholder Image 📷
- Endpoint: `/api/placeholder/<width>/<height>`
- Method: GET
- Response: A placeholder image with specified dimensions in PNG format.

---

## Usage Instructions 💡

1. Generate Text:
   - Use the `/generate-text` endpoint with a POST request containing a text prompt to get professional content.

2. Generate Images:
   - Use the `/generate-image` endpoint with a POST request containing an image prompt to get high-quality images.

3. Combined Generation:
   - Use the `/generate-both` endpoint with a POST request to receive both text and an associated image.

4. Web Interface:
   - Access `http://127.0.0.1:5000/` to use the web interface for generating text and images.

---

## Logging 📋

The application uses Python's logging module for tracking activity and errors. Logs are displayed in the console with the following levels:
- INFO: General application activity.
- ERROR: Any errors encountered during operations.

---

## Project Structure 🗂️

```
KNACK_AI_2.0/
├── app.py                 # Main application file
├── templates/
│   └── index.html         # Web interface
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```

---

## Contributing 🤝

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Create a Pull Request.

---

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for details.
