from flask import Flask, request, jsonify, render_template
from flask_material import Material
import json
import requests
from rasa.shared.core.domain import Domain

app = Flask(__name__)
Material(app)

# Define the conversational logic of your chatbot
def handle_user_input(user_input):
    if user_input.lower() in ["hello", "hi", "hey", "yo"]:
        return "Hello, I am Nova, your mental health therapist! How can I help you today?"
    elif user_input.lower() in ["goodbye", "bye", "see you later"]:
        return "Goodbye! Take care of yourself. Feel free to return if you need more support."
    elif user_input.lower() in ["what can you do?", "tell me your capabilities"]:
        return "I can answer your questions and provide support about mental health issues."
    elif user_input.lower() in ["i need help", "can you help me?", "help me"]:
        return "I am here for you. Please tell me what is bothering you."
    else:
        # Generate a response using Palm
        palm_response = call_palm_api(user_input)

        # Return the Palm response
        return palm_response

# Define a function to call the Palm API
def call_palm_api(prompt):
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "prompt": {
            "text": prompt + "( You are a mental health AI powered companion, Nova. Answer questions like you are their friend.)"
        },
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={{key}}",
        headers=headers,
        json=data,
    )

    try:
        response_data = response.json()
        return response_data['candidates'][0]['output']
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return "An error occurred while processing your request."

@app.route('/api/chat', methods=['POST'])
def chat():
    user_data = json.loads(request.data)
    user_input = user_data.get("user_input", "")
    bot_response = handle_user_input(user_input)
    return jsonify({"response": bot_response})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_interface():
    return render_template('chat.html')

@app.route('/info')
def info():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
