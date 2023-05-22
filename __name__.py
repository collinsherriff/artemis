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
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('tmp/')    
        
    code = ''
    for filename in os.listdir('tmp'):
        with open(os.path.join('tmp', filename), 'r') as f:
            code += f.read()  
            
    response = requests.post('https://api.openai.com/v1/engines/chatgpt/completions',   
        headers = {'Authorization': f'Bearer {API_KEY}'},
        data = {'prompt': code}
    )
    
    return response.json()['choices'][0]['text'] 