# chartRAG

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
