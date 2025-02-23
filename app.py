from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import pandas as pd
from openai import OpenAI
import os
import secrets
from graph import get_graph_recommendation, generate_graph

secret = secrets.token_urlsafe(32)

app = Flask(__name__)

app.secret_key = secret

# Load your OpenAI API key from an environment variable for security
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Global variable to store the data DataFrame
data_df = None
description = None

@app.route('/')
def base():
    return render_template('upload.html')

@app.route('/details')
def details():
    print("second")
    print(description)
    fig = generate_graph(data_df, get_graph_recommendation(description))
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return render_template('details.html', graph_html=graph_html)

@app.route('/upload', methods=['POST'])
def upload_file():
    global data_df
    global description
    file = request.files['datafile']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    data_df = pd.read_csv(file)
    description = data_df.describe().to_string()
    print("first")
    print(description)
    prompt=f"Summarize this data: {description}"
    
    # Generate summary with OpenAI
    summary = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    flash(summary.choices[0].message.content)  # Use flash to pass data to another route
    return redirect('/details')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json.get('question', '')
    print(question)
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    if data_df is None:
        return jsonify({'error': 'No data loaded'}), 400
    description = data_df.describe().to_string()
    prompt=f"Question: {question}\n\nData Summary:\n{data_df}\n\nAnswer:"
    
    # Simulating a response based on data summary, you could extend this to use OpenAI based on user questions
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    print(response.choices[0].message.content)
    return {'answer' : response.choices[0].message.content}


if __name__ == '__main__':
    app.run(debug=True)
