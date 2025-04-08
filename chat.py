import os 
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(prompt):
    """
    Function to interact with OpenAI's GPT-3.5-turbo model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a database expert. The user will be asking you questions about their CSV that they have uploaded. You will be providing them with what they want For example, they might ask you, what are my top 5 highest grossing movies? You will then look into the database and provide them with the answer that makes it look all nice and clean in the terminal"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )       
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
print(get_response("What is the capital of France?"))