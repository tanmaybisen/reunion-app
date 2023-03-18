# <Docker File>

# Use Python Alpine runtime as the base image for [LOW SIZE]
FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /reunion

# Copy the contents of the src directory into the container at /app
COPY src /reunion

# Install the required packages
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Specify the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
