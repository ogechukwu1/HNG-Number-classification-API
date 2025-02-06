from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is a perfect number."""
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(n):
    """Fetch a fun fact from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available")
    except:
        return "No fun fact available"
    return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Get the 'number' query parameter from the request
    number = request.args.get('number')

    # Validate that the number is provided and is a valid integer
    if number is None or not number.isdigit():
        return jsonify({"error": "Invalid input. Please provide a valid number."}), 400

    number = int(number)
    
    # Initialize an empty list to store the properties of the number
    properties = []
    
    # Check if the number is an Armstrong number
    if is_armstrong(number):
        properties.append("armstrong")
    
    # Check if the number is even or odd
    properties.append("odd" if number % 2 else "even")
    
    # Prepare the result to return as a JSON response
    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(number)),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)

