FROM python:3-alpine

# Set the working directory to /backend_service
WORKDIR /backend_service

# Install any needed packages specified in requirements.txt
COPY . .
RUN pip install -r requirements.txt

CMD python manage.py migrate && gunicorn nearby_mongodb.wsgi -b 0.0.0.0:8000
