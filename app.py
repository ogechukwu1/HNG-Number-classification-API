from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect (sum of divisors equals the number)"""
    return n == sum([i for i in range(1, n) if n % i == 0])

def is_armstrong(n):
    """Check if a number is an Armstrong number"""
    digits = [int(digit) for digit in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@app.get("/api/classify-number/{number}")
def classify_number(number: int):
    """Classify a number and return its mathematical properties"""
    try:
        number = int(number)
        properties = []
        
        if is_armstrong(number):
            properties.append("armstrong")
        
        properties.append("odd" if number % 2 != 0 else "even")
        
        # Fetch a fun fact from the Numbers API
        fun_fact_response = requests.get(f"http://numbersapi.com/{number}/math")
        fun_fact = fun_fact_response.text if fun_fact_response.status_code == 200 else "No fun fact available."

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(number)),
            "fun_fact": fun_fact
        }

    except ValueError:
        raise HTTPException(status_code=400, detail={"number": str(number), "error": True})
