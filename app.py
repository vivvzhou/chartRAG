from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()  # Get data posted as JSON
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        # Use the chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ensure this is a valid model ID for chat
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({'response': response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/")
def home():
    return "Hello, Flask!"
