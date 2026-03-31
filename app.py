from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Allow CORS for the frontend on port 8000
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY is not set in environment or .env file.")

prompt_template = """
SYSTEM:
You are a cybersecurity AI that detects phishing and scam messages in multiple languages including English, Hindi, and Malayalam.
{translation_instruction}

USER INPUT:
{user_input}

INSTRUCTIONS:
- Detect the language of the input
- Analyze the message for phishing or scam intent
- Understand cultural and regional scam patterns
- Identify urgency, manipulation, fake links, or threats
- Compare the input with a typical trusted message
- Identify differences in tone, domain, intent, and structure
- Return concise comparison points
- Translate internally if needed for better analysis

OUTPUT FORMAT (STRICT JSON ONLY, DO NOT USE MARKDOWN BLOCKS):
{{
  "language": "Detected language (e.g. English, Hindi, Malayalam)",
  "risk": "Safe" | "Suspicious" | "Scam",
  "score": 0,
  "scam_type": "string",
  "reasons": ["reason1", "reason2"],
  "highlighted_phrases": ["phrase1", "phrase2"],
  "advice": "string",
  "impact": "What could happen if the user falls for this?",
  "simple_explanation": "Explain this in extremely simple, non-technical language for a 10 year old.",
  "comparison": [
    {{
      "feature": "Domain or Tone or Intent etc.",
      "trusted": "What a trusted version would look like",
      "input": "What the user's input actually looks like"
    }}
  ]
}}
"""

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    input_type = data.get('type')
    content = data.get('content')
    language = data.get('language', 'Auto Detect')
    
    if language == 'Auto Detect':
        trans_inst = "IMPORTANT: Detect the language of the USER INPUT. Your entire JSON response (reasons, advice, impact, simple_explanation) MUST be translated into and output in that exact detected language."
    else:
        trans_inst = f"IMPORTANT: Your entire JSON response MUST be translated into and output in {language}."
    
    if not content:
        return jsonify({"error": "No content provided"}), 400
        
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        if input_type == 'image':
            if ',' in content:
                content = content.split(',')[1]
                
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64decode(content)
                }
            ]
            prompt = prompt_template.format(user_input="Please analyze the text and context inside this image for scams or phishing.", translation_instruction=trans_inst)
            response = model.generate_content([prompt, image_parts[0]])
            
        else:
            prompt = prompt_template.format(user_input=content, translation_instruction=trans_inst)
            response = model.generate_content(prompt)
            
        # Parse output
        text = response.text.strip()
        # Clean any markdown block formatting that might sneak in
        if text.startswith('```json'): text = text[7:]
        if text.startswith('```'): text = text[3:]
        if text.endswith('```'): text = text[:-3]
        
        result = json.loads(text.strip())
        
        return jsonify(result)

    except Exception as e:
        print("Analysis Error:", e)
        # Fallback response for demo safety in case API fails
        return jsonify({
            "risk": "Error",
            "score": 0,
            "scam_type": "Unknown",
            "reasons": ["Failed to connect to AI engine or parse response: " + str(e)],
            "highlighted_phrases": [],
            "advice": "Please check your API key and server connection."
        }), 500

log_prompt_template = """
SYSTEM:
You are a cybersecurity AI specialized in detecting anomalies in system logs.
IMPORTANT: Translate your response and all output into {language}.

USER INPUT:
{logs}

INSTRUCTIONS:
- Identify unusual patterns
- Detect suspicious behavior (location changes, brute force attempts, odd timing)
- Be precise and realistic

OUTPUT FORMAT (STRICT JSON ONLY, DO NOT USE MARKDOWN BLOCKS):
{{
  "risk": "Safe" | "Suspicious" | "Critical",
  "score": 0,
  "anomalies": [
    "Anomaly 1",
    "Anomaly 2"
  ],
  "explanation": "Short explanation",
  "impact": "What could happen if left unchecked?",
  "simple_explanation": "Explain this anomaly in extremely simple, non-technical language."
}}
"""

@app.route('/analyze-logs', methods=['POST'])
def analyze_logs():
    data = request.json
    logs_content = data.get('logs')
    language = data.get('language', 'English')
    
    if not logs_content:
        return jsonify({"error": "No logs provided"}), 400
        
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = log_prompt_template.format(logs=logs_content, language=language)
        response = model.generate_content(prompt)
        
        text = response.text.strip()
        if text.startswith('```json'): text = text[7:]
        if text.startswith('```'): text = text[3:]
        if text.endswith('```'): text = text[:-3]
        
        result = json.loads(text.strip())
        return jsonify(result)
        
    except Exception as e:
        print("Log Analysis Error:", e)
        return jsonify({
            "risk": "Error",
            "score": 0,
            "anomalies": ["Failed to connect to AI engine or parse response: " + str(e)],
            "explanation": "Please check your API key and server connection."
        }), 500

media_prompt_template = """
SYSTEM:
You are an AI expert in detecting manipulated and AI-generated media.
IMPORTANT: Translate your response and all output into {language}.

INSTRUCTIONS:
- Analyze for signs of deepfake or manipulation
- Look for inconsistencies in lighting, facial features, textures
- Be cautious and realistic (do not overclaim)
- Provide clear reasoning

OUTPUT FORMAT (STRICT JSON ONLY, DO NOT USE MARKDOWN BLOCKS):
{{
  "risk": "Safe" | "Suspicious" | "Manipulated",
  "score": 0,
  "findings": [
    "Finding 1",
    "Finding 2"
  ],
  "explanation": "Short explanation",
  "advice": "Short safety recommendation",
  "impact": "What could be the impact of this manipulated media?",
  "simple_explanation": "Explain what is wrong with the image in extremely simple language."
}}
"""

@app.route('/analyze-media', methods=['POST'])
def analyze_media():
    data = request.json
    content = data.get('content')
    language = data.get('language', 'English')
    
    if not content:
        return jsonify({"error": "No image provided"}), 400
        
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        if ',' in content:
            content = content.split(',')[1]
            
        image_parts = [{"mime_type": "image/jpeg", "data": base64.b64decode(content)}]
        
        prompt = media_prompt_template.format(language=language)
        response = model.generate_content([prompt, image_parts[0]])
        
        text = response.text.strip()
        if text.startswith('```json'): text = text[7:]
        if text.startswith('```'): text = text[3:]
        if text.endswith('```'): text = text[:-3]
        
        result = json.loads(text.strip())
        return jsonify(result)
        
    except Exception as e:
        print("Media Analysis Error:", e)
        return jsonify({
            "risk": "Error",
            "score": 0,
            "findings": ["Failed to connect to AI engine or parse response: " + str(e)],
            "explanation": "Please check your API key and server connection.",
            "advice": "Contact support if issue persists."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
