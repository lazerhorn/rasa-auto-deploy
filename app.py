from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

rasa_api = "http://localhost:5005/webhooks/rest/webhook"

# Simple chatbot logic
def get_bot_response(user_input):
    user_input = user_input.lower()
    response = requests.post(rasa_api , json={'message': user_input})
    print(f'Rasa1: {response}')
    response = response.json()
    print(f'Rasa2: {response}')
    response = " ".join([obj['text'] for obj in response])
    print(f'After the else: {response}')
    return response 

    # if 'hello' in user_input:
    #     return "Hi there! How can I help you today?"
    # elif 'how are you' in user_input:
    #     return "I'm just a bot, but thanks for asking!"
    # elif 'bye' in user_input:
    #     return "Goodbye! Have a great day!"
    # else:
    #     return "I'm still learning. Can you rephrase that?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = get_bot_response(user_input)
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)