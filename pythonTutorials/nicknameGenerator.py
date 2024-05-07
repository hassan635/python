import os
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def nickNameGenerator():
    name = input("Enter your name: ")
    if re.search(r'\d', name):
        print("Invalid name as provided name has numbers in it. Please try again.")
    elif re.search(r'[^a-zA-Z\s]', name):
        print("Invalid name as provided name has special characters in it. Please try again.")
    else:
        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                        {
                            "role": "user",
                            "content": f"Generate a nickname for this name: {name}. Only answer with nickname",
                        },
                    ],
            )
            nickName = response.choices[0].message.content
            print( f"Nickname for {name} is {nickName}.")
        
        except Exception as e:
            print( f"Failed to generate nickname: {str(e)}" )

def main():
    nickNameGenerator()

if __name__ == "__main__":
    main()
