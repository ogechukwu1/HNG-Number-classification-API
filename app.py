from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        return "The request to NumbersAPI timed out."
    except requests.exceptions.HTTPError:
        return "Could not retrieve fact due to a server error."
    except requests.exceptions.RequestException:
        return "Fun fact unavailable."

# Endpoints
@app.get("/")
def root():
    return {"message": "Number Classification API is running!"}

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    properties = ["even" if number % 2 == 0 else "odd"]
    
    armstrong_check = is_armstrong(number)
    if armstrong_check:
        properties.append("armstrong")

    fun_fact = get_fun_fact(number)
    
    # If Armstrong, override fun_fact with explanation
    if armstrong_check:
        digits = [int(d) for d in str(number)]
        power = len(digits)
        fun_fact = f"{number} is an Armstrong number because " + " + ".join(f"{d}^{power}" for d in digits) + f" = {number}"
    
    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": fun_fact
    }

    return result

