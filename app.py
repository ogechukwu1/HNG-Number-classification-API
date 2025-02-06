from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from utils import is_prime, is_perfect, is_armstrong, get_digit_sum

app = Flask(__name__)

# Enable CORS for all routes and all domains
CORS(app)

@app.route('/')
def home():
    return 'Welcome to the Number Classification API!'

@app.route('/is_prime', methods=['GET'])
def check_prime():
    try:
        number = int(request.args.get('number'))
        result = is_prime(number)
        return jsonify({'number': number, 'is_prime': result}), 200
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide a valid integer.'}), 400

@app.route('/is_perfect', methods=['GET'])
def check_perfect():
    try:
        number = int(request.args.get('number'))
        result = is_perfect(number)
        return jsonify({'number': number, 'is_perfect': result}), 200
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide a valid integer.'}), 400

@app.route('/is_armstrong', methods=['GET'])
def check_armstrong():
    try:
        number = int(request.args.get('number'))
        result = is_armstrong(number)
        return jsonify({'number': number, 'is_armstrong': result}), 200
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide a valid integer.'}), 400

@app.route('/digit_sum', methods=['GET'])
def digit_sum():
    try:
        number = int(request.args.get('number'))
        result = get_digit_sum(number)
        return jsonify({'number': number, 'digit_sum': result}), 200
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide a valid integer.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
