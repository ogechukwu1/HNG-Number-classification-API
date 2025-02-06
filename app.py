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
        return False  # Handle non-positive numbers
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n
def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(digit) for digit in str(n)]
    return sum(d ** len(digits) for d in digits) == n
def digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = int(request.args.get('number'))
    except (ValueError, TypeError):
        return jsonify({"number": "alphabet", "error": True}), 400
    # Calculate properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    odd = number % 2 != 0
    properties = []
    if armstrong:
        properties.append("armstrong")
    if odd:
        properties.append("odd")
    else:
        properties.append("even")
    # Fetch the fun fact from Numbers API
    fun_fact_response = requests.get(f"http://numbersapi.com/{number}?json")
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
