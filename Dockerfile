# Use a Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./init /app

# Echo the result of `ls -a`
RUN echo "Listing all files and directories in /app:" && ls -a /app

# Install any necessary Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "-m", "scripts.main"]
