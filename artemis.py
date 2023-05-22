import zipfile
import requests

# HTML form will submit to this route 
@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the .zip file from the request
    zip_file = request.files['code_zip']
    
    # Extract the .zip to a temporary directory
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('tmp/')
        
    # Read all the files in the tmp dir and join the text    
    code = ''
    for filename in os.listdir('tmp'):
        with open(os.path.join('tmp', filename), 'r') as f:
            code += f.read()
            
    # Make request to OpenAI API
    response = requests.post('https://api.openai.com/v1/engines/chatgpt/completions', 
        headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'},
        data = {'prompt': code}
    )
    
    # Return API response to user
    return response.json()['choices'][0]['text']