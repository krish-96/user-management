# Use the official Ubuntu base image
#FROM ubuntu:24.04
FROM python:3.12-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies and Python 3.12
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends build-essential software-properties-common byobu curl  git htop  man unzip vim  wget  ca-certificates python3-launchpadlib && \
#    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /django_app

ENV PYTHONPATH=/django_app

# Add files to the container
COPY requirements.txt /django_app/

# Upgrade pip and install dependencies (use --break-system-packages)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /django_app/

# Create log directory with correct permissions
RUN mkdir -p /var/log/k8s_auth && \
    chown -R 1000:1000 /var/log/k8s_auth && \
    chmod 755 -R /var/log/k8s_auth

# Expose the application port
EXPOSE 8008

# Content
RUN echo "Content in the dir" && pwd && ls -lh


# Collect static files
RUN python manage.py collectstatic --noinput

# Define the entrypoint
#ENTRYPOINT []
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8008", "k8s_auth.wsgi:application"]
