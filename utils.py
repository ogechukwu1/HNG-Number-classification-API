# utils.py
def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number):
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def is_armstrong(number):
    digits = [int(d) for d in str(number)]
    return sum(d ** len(digits) for d in digits) == number

def get_digit_sum(number):
    return sum(int(d) for d in str(number))
