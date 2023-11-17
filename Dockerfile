# Use the official Python image as a base image
FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/


# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kanban_project.wsgi:application"]
