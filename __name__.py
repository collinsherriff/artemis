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
    zip_file = request.files['code_zip']   
    
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
    
    # Return response
    return response.json()['choices'][0]['text']

if __name__ == "__main__":
    app.run(debug=True ,port=3000,use_reloader=False)