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
    digits = [int(digit) for digit in str(abs(n))]  # Handle negative numbers
    return sum(d ** len(digits) for d in digits) == abs(n)

def digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    
    # Validate input
    try:
        number = float(number_str) if '.' in number_str else int(number_str)
    except (ValueError, TypeError):
        return jsonify({"number": number_str, "error": True, "message": "Invalid input"}), 400

    # Determine properties
    prime = is_prime(int(number))
    perfect = is_perfect(int(number))
    armstrong = is_armstrong(int(number))
    odd = int(number) % 2 != 0

    properties = []
    if armstrong:
        properties.append("armstrong")
    if odd:
        properties.append("odd")
    else:
        properties.append("even")

    # Fetch fun fact (Handle API failure gracefully)
    fun_fact = f"No fun fact available for {number}"
    try:
        response = requests.get(f"http://numbersapi.com/{int(number)}?json", timeout=5)
        if response.status_code == 200:
            fun_fact = response.json().get('text', fun_fact)
    except requests.exceptions.RequestException:
        pass  # Keep default fun fact message

    # Prepare response
    response = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum(int(number)),
        "fun_fact": fun_fact
    }

    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT automatically
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


