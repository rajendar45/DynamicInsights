# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Install the dependencies
RUN pip install flask flask-cors


# Copy the application code into the container
COPY . /app/
# Expose the port that the application will run on
EXPOSE 8080

# Run the command to start the application when the container launches
CMD ["python3", "DynamicInsightsRestServcie.py"]