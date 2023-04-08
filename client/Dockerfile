FROM python:3

WORKDIR /app


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for client data
VOLUME /clientdata

COPY . .

# Set the default command to run the client application
CMD ["python", "client.py"]
