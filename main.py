import requests
import json
from rasa.shared.core.domain import Domain
from rasa_sdk import Action
# Define the intents and entities of your chatbot
domain = Domain.load("domain.yml")



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
            "text": prompt + "( You are a mental health AI powered companion. Answer questions like you are their frind.)"
        },
    }

    print(data)

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key=AIzaSyD_q04TyZBH7hH-eVzh5RT0ej4jGkcPF4k",
        headers=headers,
        json=data,
    )

    try:
        print(response.json())
        response_data = response.json()
        return response_data['candidates'][0]['output']
    except json.JSONDecodeError as e:
        # Handle the JSONDecodeError
        print(f"Error decoding JSON response: {e}")
        return "An error occurred while processing your request."

# Start the chatbot loop
while True:
    user_input = input("You: ")
    response = handle_user_input(user_input)
    print("Nova:", response)
