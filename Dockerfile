# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY pdf_image_extractor.py .

# Set the command to run the Python script
CMD ["python", "pdf_image_extractor.py", "/app/pdf_files"]
