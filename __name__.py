import os
from dotenv import load_dotenv
import zipfile 
import requests
from flask import Flask, request

load_dotenv()
API_KEY = os.environ.get('API_KEY')

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])  
def analyze():
    try:
        zip_file = request.files['code_zip']
        print("Received ZIP file:", zip_file.filename)

        # Extract the zip file 
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('tmp/')    

        # Get the full code string 
        code = ''
        for filename in os.listdir('tmp'):
            with open(os.path.join('tmp', filename), 'r') as f:
                code += f.read()  

        # Make request to OpenAI API    
        response = requests.post('https://api.openai.com/v1/engines/chatgpt/completions',   
            headers = {'Authorization': f'Bearer {API_KEY}'},
            data = {'prompt': code}
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
    app.run(debug=True, port=3000, use_reloader=False)
