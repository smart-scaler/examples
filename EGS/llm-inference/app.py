from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the Hugging Face text generation pipeline with the GPT-2 model
model = pipeline('text-generation', model='gpt2')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('input', '')
    
    # Generate text with a max length of 100 tokens
    try:
        result = model(text, max_length=100, num_return_sequences=1)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
