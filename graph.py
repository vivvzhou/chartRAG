import plotly.express as px
import pandas as pd
from openai import OpenAI
import os

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def get_graph_recommendation(description):
    print(description)
    prompt=f"Recommend a graph for this data to best represent the data: {description}. Only write one word"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    print(response.choices[0].message.content)
    print("wow")
    return response.choices[0].message.content

def generate_graph(data, graph_type):
    prompt=f"Generate a title for a graph of {graph_type} type with this data: {data}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    if 'line' == graph_type:
        # Assuming 'data' is a DataFrame with a DateTime index and multiple columns for data
        fig = px.line(data, x=data.index, y=data.columns, title=response.choices[0].message.content)
        return fig

    elif 'bar' == graph_type:
        # Assuming 'data' has categorical data in the first column and values in the second
        fig = px.bar(data, x=data[data.columns[0]], y=data[data.columns[1]], title=response.choices[0].message.content)
        return fig
    
    else:
        fig = px.bar(data, x=data[data.columns[1]], y=data[data.columns[2]], title=response.choices[0].message.content)
        return fig