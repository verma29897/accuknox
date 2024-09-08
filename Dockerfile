
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /accounts

# Install dependencies
COPY requirements.txt /accounts//
RUN pip install -r requirements.txt

# Copy the project files to the container
COPY . /accounts/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
