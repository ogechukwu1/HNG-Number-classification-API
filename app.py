import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Helper functions to determine properties of a number
def is_prime(n):
    if n <= 1 or not isinstance(n, int):
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n <= 0 or not isinstance(n, int):
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def is_armstrong(n):
    if n < 0 or not isinstance(n, int):
        return False
    digits = [int(digit) for digit in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def digit_sum(n):
    if not isinstance(n, int):
        return None  # Prevent errors for non-integer values
    return sum(int(digit) for digit in str(abs(n)))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    
    try:
        number = float(number_str)
        if number.is_integer():
            number = int(number)  # Convert float to int if it's a whole number
        else:
            return jsonify({"error": "Only whole numbers are supported"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. Please provide a valid number"}), 400

    # Calculate properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    odd = number % 2 != 0
    properties = ["odd" if odd else "even"]
    
    if armstrong:
        properties.append("armstrong")
    
    # Fetch fun fact from Numbers API
    fun_fact = f"No fun fact available for {number}"
    try:
        response = requests.get(f"http://numbersapi.com/{number}?json", timeout=5)
        if response.status_code == 200:
            fun_fact = response.json().get('text', fun_fact)
    except requests.RequestException:
        pass  # If the request fails, use the default fun fact message

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