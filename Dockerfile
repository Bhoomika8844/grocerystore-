FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY templates/ ./templates/
COPY tests/ ./tests/ 

RUN pip install --no-cache-dir flask && \
    touch products.db && \
    chmod a+rw products.db

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]