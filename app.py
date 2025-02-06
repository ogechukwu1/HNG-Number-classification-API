from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from utils import is_prime, is_perfect, is_armstrong, get_digit_sum

app = Flask(__name__)

# Enable CORS for all routes and all domains
CORS(app)

@app.route('/')
def home():
    return 'Welcome to the Number Classification API!'

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = int(request.args.get('number'))
        
        # Call the classification functions and store results
        prime_result = is_prime(number)
        perfect_result = is_perfect(number)
        armstrong_result = is_armstrong(number)
        digit_sum_result = get_digit_sum(number)

        # Return results in a JSON response
        return jsonify({
            'number': number,
            'is_prime': prime_result,
            'is_perfect': perfect_result,
            'is_armstrong': armstrong_result,
            'digit_sum': digit_sum_result
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid input, please provide a valid integer.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
