import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Helper functions
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
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(digit) for digit in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number')

    if number_param is None:
        return jsonify({"error": "Missing 'number' parameter"}), 400

    try:
        number = int(number_param)
    except ValueError:
        return jsonify({"error": "Invalid input. Please provide a valid number."}), 400

    # Calculate properties
    properties = {
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "is_armstrong": is_armstrong(number),
        "is_odd": number % 2 != 0,
        "digit_sum": digit_sum(number)
    }
    
    properties["parity"] = "odd" if properties["is_odd"] else "even"

    # Fetch fun fact (Handle API failure)
    fun_fact = f"No fun fact available for {number}"
    try:
        response = requests.get(f"http://numbersapi.com/{number}?json", timeout=5)
        if response.status_code == 200:
            fun_fact = response.json().get('text', fun_fact)
    except requests.RequestException:
        pass  # Keep default fun fact

    return jsonify({
        "number": number,
        **properties,
        "fun_fact": fun_fact
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


