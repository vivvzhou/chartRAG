from flask import Flask, request, jsonify, render_template
import pandas as pd
from openai import OpenAI
import os

app = Flask(__name__)

# Load your OpenAI API key from an environment variable for security
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Global variable to store the data DataFrame
data_df = None

@app.route('/')
def base():
    return render_template('upload.html')

@app.route('/details')
def details():
    return render_template('details.html')

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
    summary = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return summary.choices[0].message.content

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    if data_df is None:
        return jsonify({'error': 'No data loaded'}), 400
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
