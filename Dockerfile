# Use an official slim Python 3.12 base image to keep the image size small
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the port Flask/Gunicorn will listen on
EXPOSE 5000

# Run the app with Gunicorn in production mode
# -w 2  : two worker processes
# -b    : bind to all interfaces on port 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]
