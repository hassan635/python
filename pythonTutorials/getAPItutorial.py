from flask import Flask, request, jsonify, make_response
import random

app = Flask(__name__)

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# List of 10 motivational quotes
quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only way to achieve the impossible is to believe it is possible. - Charles Kingsleigh",
    "Act as if what you do makes a difference. It does. - William James",
    "Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
    "Keep your face always toward the sunshine - and shadows will fall behind you. - Walt Whitman",
    "The best way to predict the future is to create it. - Peter Drucker"
]

@app.route('/get_quote', methods=['GET'])
def get_quote():
    # Randomly select a quote from the list
    random_quote = random.choice(quotes)
    return jsonify({'quote': random_quote})

if __name__ == "__main__":
    app.run(debug=True)