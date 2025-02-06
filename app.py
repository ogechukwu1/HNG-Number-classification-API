from flask import Flask, request, jsonify
import requests
from utils import is_prime, is_perfect, is_armstrong, get_digit_sum

app = Flask(__name__)

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = int(request.args.get('number'))
    except (ValueError, TypeError):
        return jsonify({"number": request.args.get('number'), "error": True}), 400

    properties = []

    # Check for Armstrong, Prime, and Perfect properties
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")

    # Get digit sum
    digit_sum = get_digit_sum(number)

    # Get fun fact using Numbers API
    fun_fact_response = requests.get(f'http://numbersapi.com/{number}/math?json=true')
    fun_fact = fun_fact_response.json().get("text", "No fun fact available.")

    return jsonify({
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    })

if __name__ == '__main__':
    app.run(debug=True)
