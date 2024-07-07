# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    default-libmysqlclient-dev \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV PORT 5006

# Expose the port the app runs on
EXPOSE $PORT

# Run the application
CMD ["gunicorn", "hbnb:app", "-w", "2", "-b", "0.0.0.0:$PORT"]

