from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = list(map(int, str(n)))
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num = request.args.get('number')

    if not num or not num.isdigit():
        return jsonify({"number": num, "error": True}), 400

    num = int(num)
    properties = ["odd" if num % 2 else "even"]
    
    if is_armstrong(num):
        properties.insert(0, "armstrong")

    response = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": num == sum(i for i in range(1, num) if num % i == 0),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(num)),
        "fun_fact": get_fun_fact(num)
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
