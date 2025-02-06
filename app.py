import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Helper functions to determine properties of a number
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 0:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(digit) for digit in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')

    # Handle missing number
    if number_str is None:
        return jsonify({"number": None, "error": "Missing number parameter"}), 400

    # Try to parse the number (handle integers and floats)
    try:
        number = float(number_str)
        if number.is_integer():
            number = int(number)  # Convert float-like integers to int
    except ValueError:
        return jsonify({"number": number_str, "error": "Invalid input"}), 400

    # Calculate properties
    prime = is_prime(number) if isinstance(number, int) else False
    perfect = is_perfect(number) if isinstance(number, int) else False
    armstrong = is_armstrong(number) if isinstance(number, int) else False
    odd = number % 2 != 0 if isinstance(number, int) else None

    properties = []
    if armstrong:
        properties.append("armstrong")
    if odd is not None:
        properties.append("odd" if odd else "even")

    # Fetch the fun fact from Numbers API (only for integers)
    fun_fact = None
    if isinstance(number, int):
        fun_fact_response = requests.get(f"http://numbersapi.com/{number}?json")
        if fun_fact_response.status_code == 200:
            fun_fact = fun_fact_response.json().get('text', f"No fun fact available for {number}")

    # Prepare response
    response = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": fun_fact
    }

    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
