from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import secrets
import re       # Regular expressions for markdown conversion (String -> html)
from flask_cors import CORS

secret = secrets.token_urlsafe(32)

app = Flask(__name__)

app.secret_key = secret
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from an environment variable for security
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Global variables to store the data DataFrame and summary
data_df = None
summary_content = None

# @app.route('/')
# def base():
#     return render_template('upload.html')

# @app.route('/details')
# def details():
#     return render_template('details.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global data_df, summary_content
    file = request.files['datafile']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    data_df = pd.read_csv(file)
    description = data_df.describe().to_string()
    prompt = f"Summarize this data as a structured report (with bullet points): {description}"

    # Generate summary with OpenAI
    summary = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    summary_content = summary.choices[0].message.content
    flash(summary_content)  # Use flash to pass data to another route
    # return redirect('/details')
    return jsonify({'summary': summary_content})

@app.route('/ask', methods=['POST'])
def ask_question():
    global summary_content
    question = request.json.get('question', '')
    print(question)
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    if data_df is None:
        return jsonify({'error': 'No data loaded'}), 400
    description = data_df.describe().to_string()
    prompt = f"Question: {question}\n\nSummary:\n{summary_content}\n\nData Summary:\n{description}\n\nAnswer:"

    # Generate response based on question and summary
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Try to answer the question in one sentence (300 tokens)."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    print("answer: ", response.choices[0].message.content)
    return jsonify({'answer': response.choices[0].message.content})

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data.get('message', '')
    new_message = 'hi ' + message
    return jsonify({'message': new_message})


def markdown_to_html(markdown_text):
    # Convert headers
    markdown_text = re.sub(r'###### (.+)', r'<h6>\1</h6>', markdown_text)
    markdown_text = re.sub(r'##### (.+)', r'<h5>\1</h5>', markdown_text)
    markdown_text = re.sub(r'#### (.+)', r'<h4>\1</h4>', markdown_text)
    markdown_text = re.sub(r'### (.+)', r'<h3>\1</h3>', markdown_text)
    markdown_text = re.sub(r'## (.+)', r'<h2>\1</h2>', markdown_text)
    markdown_text = re.sub(r'# (.+)', r'<h1>\1</h1>', markdown_text)

    # Convert bold text
    markdown_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', markdown_text)
    markdown_text = re.sub(r'__(.+?)__', r'<b>\1</b>', markdown_text)

    # Convert italic text
    markdown_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', markdown_text)
    markdown_text = re.sub(r'_(.+?)_', r'<i>\1</i>', markdown_text)

    # Convert new lines
    markdown_text = re.sub(r'\n', r'<br>', markdown_text)

    return markdown_text


if __name__ == '__main__':
    app.run(debug=True)
