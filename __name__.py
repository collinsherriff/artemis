import os
from dotenv import load_dotenv
import zipfile
import requests
from flask import Flask, request

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.environ.get('API_KEY')

# Create Flask application
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Retrieve the uploaded ZIP file from the request
        zip_file = request.files['code_zip']
        print("Received ZIP file:", zip_file.filename)

        # Extract the contents of the ZIP file to a temporary directory
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('tmp/')

        # Combine the code from all extracted files into a single string
        code = ''
        for filename in os.listdir('tmp'):
            with open(os.path.join('tmp', filename), 'r') as f:
                code += f.read()

        # Make a request to the OpenAI API for code completion
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {API_KEY}'},
            json={
                'prompt': code,
                'max_tokens': 100,  # Adjust as needed
                'temperature': 0.6  # Adjust as needed
            }
        )

        if response.status_code == 200:
            print("API Request Successful")
            return response.json()['choices'][0]['text']
        else:
            print("API Request Failed")
            return "Error: API request failed"

    except Exception as e:
        print("Error occurred:", str(e))
        return "Error: An unexpected error occurred"

if __name__ == "__main__":
    # Run the Flask application in debug mode on port 3000
    app.run(debug=True, port=3000, use_reloader=False)
