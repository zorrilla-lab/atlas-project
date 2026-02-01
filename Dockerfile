# python base image
FROM python:3.11-slim

# install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# replace later with main script, e.g. CMD ["python", "main.py"]
CMD ["python"]
