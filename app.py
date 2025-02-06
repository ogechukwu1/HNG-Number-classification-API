from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def is_armstrong(n):
    digits = [int(digit) for digit in str(abs(n))]
    return sum(d ** len(digits) for d in digits) == abs(n)

def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        return response.json().get("text", "No fun fact available")
    except:
        return "No fun fact available"

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    # Check if number is valid integer
    try:
        number = int(number)
    except ValueError:
        return jsonify({"number": number, "error": True}), 400

    # Number properties
    properties = ["odd" if number % 2 != 0 else "even"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")

    # Construct response
    response = {
        "number": number,
        "is_prime": number > 1 and all(number % i != 0 for i in range(2, int(abs(number) ** 0.5) + 1)),
        "is_perfect": number > 0 and sum(i for i in range(1, number) if number % i == 0) == number,
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(abs(number))),
        "fun_fact": get_fun_fact(number)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)

