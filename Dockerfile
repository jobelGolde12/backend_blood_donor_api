# Use a slim Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 10000

# Command to run the FastAPI application using Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
# The --port 10000 matches the EXPOSE instruction
# The --workers 4 flag is added for production deployment, you can adjust this based on your needs
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "4"]
