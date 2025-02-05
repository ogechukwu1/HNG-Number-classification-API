FROM python:3.8-slim

# Install NGINX
RUN apt-get update && apt-get install -y nginx

# Install Flask
RUN pip install Flask requests

# Copy Flask app and NGINX configuration
COPY . /app
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 5000

# Start NGINX and Flask
CMD service nginx start && python /app/app.py
