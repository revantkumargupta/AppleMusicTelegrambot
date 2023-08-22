# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files from the repository into the container
COPY . /app/

# Change permissions for the mp4decrypt executable
RUN chmod +x mp4decrypt

# Install gpac using apt-get
RUN apt-get update && apt-get install -y gpac

# Install any needed Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose any ports if needed
EXPOSE 8000

# Run the Python script
CMD ["python3", "telegram_bot.py"]
