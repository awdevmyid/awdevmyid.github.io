# Use a base image
FROM ubuntu:latest

# Set environment variables
ENV PACKAGE_NAME id.my.awdev
ENV PACKAGE_VERSION 1.0.0

# Set default values for environment variables
ENV CONFIG_FILE /etc/myapp/config.yaml
ENV LOG_FILE /var/log/myapp.log

# Set maintainer label
LABEL maintainer="Your Name <your.email@example.com>"

# Install necessary packages
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    package3

# Copy application files to the container
COPY . /app

# Set working directory
WORKDIR /app

# Run any necessary setup commands
RUN chmod +x setup.sh && ./setup.sh

# Expose any necessary ports
EXPOSE 8080

# Define the entrypoint command
CMD ["python", "app.py"]
