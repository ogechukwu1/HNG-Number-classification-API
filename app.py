import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Helper functions to determine properties of a number
def is_prime(n):
    if n <= 1 or not float(n).is_integer():
        return False  # Non-integer and numbers ≤1 are not prime
    n = int(n)  # Convert to integer for proper calculations
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 0 or not float(n).is_integer():
        return False  # Non-integer and negative numbers are not perfect
    n = int(n)
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n):
    if not float(n).is_integer():
        return False  # Only integers can be Armstrong numbers
    n = int(n)
    digits = [int(digit) for digit in str(abs(n))]  # Handle absolute value
    return sum(d ** len(digits) for d in digits) == n

def digit_sum(n):
    return sum(int(digit) for digit in str(abs(int(n))))  # Convert float to int for digit sum

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = float(request.args.get('number'))  # Accepts both integer and floating-point values
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input, please provide a valid number"}), 400

    # Determine properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    odd = int(number) % 2 != 0 if number.is_integer() else None  # Odd/Even only for integers

    # Prepare properties list
    properties = []
    if armstrong:
        properties.append("armstrong")
    if odd is not None:
        properties.append("odd" if odd else "even")

    # Fetch fun fact only for integers
    fun_fact = None
    if number.is_integer():
        try:
            fun_fact_response = requests.get(f"http://numbersapi.com/{int(number)}?json")
            if fun_fact_response.status_code == 200:
                fun_fact = fun_fact_response.json().get('text', f"No fun fact available for {int(number)}")
        except requests.exceptions.RequestException:
            fun_fact = "Could not retrieve fun fact"

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
