# HNG-Number-classification-API


## Deploying a Number Classification API on Render


### Introduction

I'll walk you through the process of building and deploying a Number Classification API using Flask on Render. I'll also share the challenges I faced during deployment and how I resolved them. 


Technologies Used

- Python
- Flask
- Requests
- Render (Deployment)



__SETTING UP THE PROJECT__

To start, I created a simple Flask API that classifies numbers based on different properties, such as:

- Whether the number is prime

- Whether it is a perfect number

- Whether it is an Armstrong number


__Create a Project Folder__

```
mkdir number-classification-api
cd number-classification-api

```
![](./images/1.png)


- Install [Python](https://www.python.org/downloads/) and dependencies

- Create a virtual environment and Install Flask for API development

```
python -m venv venv
venv\Scripts\activate (for windows)
pip install flask requests
```
![](./images/6.png)

- Create a Python file `app.py` and add the following code:

```
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
```

- Start the Flask server


`python app.py`

![](./images/7.png)


__Pushing to GitHub__

I created and initialized a Git repository and pushed my code to GitHub

`HNG-Number-classification-API`

- Open your terminal or command prompt and navigate to your project folder,Create a `.gitignore` file

```
git init
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ogechukwu1/HNG-Number-classification-API.git
git push -u origin main

```

![](./images/9.png)

![](./images/10.png)

![](./images/11.png)

![](./images/12.png)

![](./images/13.png)



__Preparing for Deployment on Render__

To deploy on [Render](https://dashboard.render.com/), I needed to:

- Create a requirements.txt file with all dependencies

```
annotated-types==0.7.0
anyio==4.8.0
blinker==1.9.0
boto3==1.26.137
botocore==1.29.165
certifi==2024.12.14
cffi==1.17.1
charset-normalizer==3.4.1
click==8.1.8
colorama==0.4.6
contourpy==1.3.1
cors==1.0.1
cycler==0.12.1
distlib==0.3.9
fastapi==0.115.8
filelock==3.17.0
Flask==3.1.0
Flask-Cors==5.0.0
fonttools==4.55.3
future==1.0.0
gevent==24.11.1
git-filter-repo==2.45.0
greenlet==3.1.1
gunicorn==23.0.0
h11==0.14.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.5
jmespath==1.0.1
kiwisolver==1.4.8
MarkupSafe==3.0.2
matplotlib==3.10.0
numpy==2.2.1
packaging==24.2
pandas==2.2.3
pillow==11.1.0
platformdirs==4.3.6
pycparser==2.22
pydantic==2.10.6
pydantic_core==2.27.2
pyparsing==3.2.1
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.0.0
pytz==2024.2
requests==2.28.2
requests-file==2.1.0
s3transfer==0.6.2
schedule==1.2.2
setuptools==75.8.0
six==1.17.0
sniffio==1.3.1
starlette==0.45.3
tldextract==5.1.3
typing_extensions==4.12.2
tzdata==2024.2
urllib3==1.26.20
uvicorn==0.34.0
virtualenv==20.29.1
waitress==3.0.2
Werkzeug==3.1.3
zope.event==5.0
zope.interface==7.2
```

- Click "New Web Service" and connect my GitHub repository

- Select Python as the runtime

- Set the Start Command `waitress-serve --listen=0.0.0.0:10000 app:app`

- Set up Gunicorn or Waitress as the production WSGI server (Web Server Gateway Interface)


![](./images/2.png)

![](./images/3.png)

![](./images/4.png)

![](./images/5.png)

Once deployed, you’ll get a public URL like

`http://127.0.0.1:5000/api/classify-number?number=371`



![](./images/14.png)



__challenges and Solutions__

__Error 1: Module Not Found Error__

Render was failing to install dependencies, showing this error `ModuleNotFoundError: No module named 'flask'`

__Solution__

I had forgotten to add a requirements.txt file. After adding it and pushing the changes, the error was resolved.



![](./images/16.png)


__Error 2: Application Failed to Start__


I got this error when Render tried to run my app: `No module named 'gunicorn'`

__Solution__

Since Render does not run Flask's built-in server in production, I installed waitress and used it instead of Gunicorn `pip install waitress` and updated my start command in Render to `waitress-serve --listen=0.0.0.0:10000 app:app`. Pushed the changes, and the issue was fixed.



![](./images/15.png)



__Error 3: API Not Responding__

The API deployed successfully, but requests returned a 404 error.

__Solution__

I realized I had forgotten to expose port 10000 in Render. Went to Render Dashboard → Environment Variables, Set `PORT=10000` and Redeployed the app





__Final Deployment URL__

The API is live at: https://hng-number-classification-api-m4me.onrender.com


![](./images/18.png)

![](./images/17.png)


__CONCLUSION__

This project has been an incredibly valuable learning experience, and I’m excited with how the Number Classification API has turned out. Building, deploying, and troubleshooting the API has significantly enhanced my skills in both development and deployment. The final result is a fast, reliable, and user friendly API that I’m proud of.
Throughout this journey, I gained hands on experience in deploying APIs, addressing challenges, and optimizing performance skills that are essential in the fields of [DevOps](https://hng.tech/hire/devops-engineers) and [Cloud Engineering](https://hng.tech/hire/cloud-engineers).



















































































































































































































































































































