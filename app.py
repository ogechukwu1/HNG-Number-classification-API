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
    number = request.args.get('number')

    if number is None:
        return jsonify({"error": "No number provided"}), 400

    try:
        # Try to convert to a float first to allow negative and decimal numbers
        number = float(number)
        
        # Now check for valid number types
        if number.is_integer():
            number = int(number)  # Convert to integer if it's a valid integer
            
        if number < 0:
            # You can decide if you want to include handling for negative numbers or not
            # In this case, we will proceed even if the number is negative
            properties = []
            if is_armstrong(number):
                properties.append("armstrong")
            properties.append("odd" if number % 2 else "even")
            result = {
                "number": number,
                "is_prime": is_prime(number),
                "is_perfect": is_perfect(number),
                "properties": properties,
                "digit_sum": sum(int(d) for d in str(abs(number))),
                "fun_fact": get_fun_fact(number)
            }
            return jsonify(result), 200
        else:
            properties = []
            if is_armstrong(number):
                properties.append("armstrong")
            properties.append("odd" if number % 2 else "even")
            result = {
                "number": number,
                "is_prime": is_prime(number),
                "is_perfect": is_perfect(number),
                "properties": properties,
                "digit_sum": sum(int(d) for d in str(abs(number))),
                "fun_fact": get_fun_fact(number)
            }
            return jsonify(result), 200

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
