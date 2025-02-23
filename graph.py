import plotly.express as px
import pandas as pd
from openai import OpenAI
import os
import plotly.graph_objects as go
import numpy as np

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
    prompt=f"which variable should be the best fit for the x-axis in a {graph_type} graph with this data: {data}. Make sure it is quantified. Make sure it is the exact name of the column header and it is the only word in the response"
    x = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    x_axis = x.choices[0].message.content
    prompt=f"if the graph has another variable, which variable should be the best fit for the y-axis in a {graph_type} graph with this data: {data}, and an x-axis of {x.choices[0].message.content}. Make sure it is the exact name of the column header and it is the only word in the response"
    y = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    y_axis = y.choices[0].message.content
    prompt=f"Generate a title for a graph of {graph_type} type with this data: {data} that has an x-axis of {x_axis} and a y-axis of {y_axis}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    if 'Line' == graph_type:
        fig = px.line(data, x=data[x_axis], y=data[y_axis], title=response.choices[0].message.content)
        return fig

    elif 'Bar' == graph_type:
        fig = px.bar(data, x=data[x_axis], y=data[y_axis], title=response.choices[0].message.content)
        return fig
    
    elif 'Histogram' == graph_type:
        fig = px.histogram(data, x=data[x_axis], title=response.choices[0].message.content)
        return fig
    
    elif 'Scatterplot' == graph_type:
        slope, intercept = np.polyfit(data[x_axis], data[y_axis], 1)
        line = slope * data[x_axis] + intercept
        fig = px.scatter(data, x=data[x_axis], y=data[y_axis], title=response.choices[0].message.content)
        fig.add_trace(go.Scatter(x=data[x_axis], y=line, mode='lines', name='Trendline',line=dict(color='red')))
        return fig
    
    elif 'Boxplot' == graph_type:
        fig = px.box(data, x=data[x_axis], title=response.choices[0].message.content)
        return fig

    else:
        fig = px.bar(data, x=data[x_axis], y=data[y_axis], title=response.choices[0].message.content)
        return fig