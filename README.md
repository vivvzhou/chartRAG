# chartRAG

# ChartRAG

ChartRAG is a web application that allows users to upload CSV files, generate data summaries, and ask questions about the data using OpenAI's language models. The application is built using Flask and provides an intuitive web interface for data interaction.

## Features

- **CSV File Upload**: Users can upload CSV files through the web interface. The application reads the file and processes the data using Pandas.
- **Data Summary**: The application generates a statistical summary of the uploaded data and uses OpenAI's API to create a natural language summary.
- **Question and Answer**: Users can ask questions about the data, and the application provides answers based on the data summary using OpenAI's models.
- **Web Interface**: The application includes HTML templates for uploading files and viewing data summaries and answers.

## Technologies Used

- **Flask**: A lightweight web framework for building the server and handling HTTP requests.
- **Pandas**: A data analysis library for reading and summarizing CSV files.
- **OpenAI API**: Used to generate data summaries and answer questions.
- **Python-dotenv**: For loading environment variables, including the OpenAI API key.

## Setup

1. **Install Dependencies**: Ensure you have Python installed, then run `pip install -r requirements.txt` to install the necessary packages.
2. **Environment Variables**: Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```
3. **Run the Application**: Start the Flask server by running `python app.py`. Access the application in your web browser at `http://localhost:5000`.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd chartRAG
   ```

2. **Set up a virtual environment:**

   Make sure you have Python and pip installed. Then create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   With the virtual environment activated, run:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. **Set the OpenAI API Key:**

   You can set the OpenAI API key as an environment variable. Here are some methods:

   - **On macOS/Linux with Bash or Zsh:**

     Add the following line to your `~/.bashrc` or `~/.zshrc` file:

     ```bash
     export OPENAI_API_KEY='your-api-key'
     ```

     Reload your shell configuration:

     ```bash
     source ~/.bashrc
     ```
     or
     ```bash
     source ~/.zshrc
     ```

   - **On Windows with Command Prompt:**

     ```cmd
     set OPENAI_API_KEY=your-api-key
     ```

   - **On Windows with PowerShell:**

     ```powershell
     $env:OPENAI_API_KEY='your-api-key'
     ```

   - **Using a `.env` File:**

     Create a file named `.env` in your project directory and add:

     ```
     OPENAI_API_KEY=your-api-key
     ```

     Use `python-dotenv` to load the environment variables in your `app.py`:

     ```python
     from dotenv import load_dotenv
     load_dotenv()
     ```

2. **Run the application:**

   Start the Flask application:

   ```bash
   python app.py
   ```

3. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:5000/` to access the application.

## Docker Deployment

To build and run the backend using Docker, follow these steps:

1. **Build the Docker image:**

   ```bash
   cd backend
   docker build -t chart-rag-backend .
   ```

2. **Run the Docker container with the `OPENAI_API_KEY` attached as an environment variable:**

   ```bash
   docker run -p 5000:5000 -e OPENAI_API_KEY=your-api-key chart-rag-backend
   ```

   Replace `your-api-key` with your actual OpenAI API key.

3. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:5000/` to access the application running inside the Docker container.

## Heroku Deployment

You can deploy the application to Heroku using Docker containers. Follow the steps below:

1. **Login to Heroku and Container Registry:**

   ```bash
   heroku login
   heroku container:login
   ```

2. **Create a Heroku App:**

   ```bash
   heroku create
   ```

   This will create a new Heroku app and provide the app name and Git URL.

3. **Set the Stack to Container:**

   ```bash
   heroku stack:set container -a your-app-name
   ```

   Replace `your-app-name` with the name of your Heroku app.

4. **Push the Docker Container:**

   Navigate to the `backend` directory and push the Docker container:

   ```bash
   cd backend
   heroku container:push web -a your-app-name
   ```

5. **Release the Container:**

   ```bash
   heroku container:release web -a your-app-name
   ```

6. **Set Environment Variables:**

   Set the `OPENAI_API_KEY` config variable on Heroku:

   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key -a your-app-name
   ```

7. **Access the Application:**

   Open the application in your web browser:

   ```bash
   heroku open -a your-app-name
   ```

**Note:** Ensure that you have the Heroku CLI installed and Docker properly set up on your machine.
