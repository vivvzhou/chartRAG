from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import openai
import os

app = Flask(__name__)

# Load your OpenAI API key from an environment variable for security
openai.api_key = os.getenv('OPENAI_API_KEY')

# Global variable to store the data DataFrame
data_df = None

@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global data_df
    file = request.files['datafile']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    data_df = pd.read_csv(file)
    description = data_df.describe().to_string()
    prompt=f"Summarize this data: {description}"
    
    # Generate summary with OpenAI
    summary = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return jsonify({'summary': summary['choices'][0]['message']['content']})

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    if data_df is None:
        return jsonify({'error': 'No data loaded'}), 400
    file = request.files['datafile']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    data_df = pd.read_csv(file)
    description = data_df.describe().to_string()
    prompt=f"Question: {question}\n\nData Summary:\n{description}\n\nAnswer:"
    
    # Simulating a response based on data summary, you could extend this to use OpenAI based on user questions
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    print({'answer': response.choices[0].text})
    return {'answer': response.choices[0].text}

if __name__ == '__main__':
    app.run(debug=True)
