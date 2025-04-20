FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY templates/ ./templates/

# Set the Flask app environment variable
ENV FLASK_APP=app.py

# Install Flask
RUN pip install --no-cache-dir flask

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
