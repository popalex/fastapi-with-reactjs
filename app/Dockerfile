# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the image
COPY . /app

# Expose the port FastAPI runs on
EXPOSE 8000

WORKDIR /

# app -> module
# main -> main.py file
# app -> fastapi variable

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
