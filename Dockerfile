# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# COPY current directory code to /app in the container
COPY ./backend /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn uvicorn[standard] openai

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ws", "websockets"]
