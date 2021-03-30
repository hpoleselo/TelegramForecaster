FROM python:3.8-slim-buster

WORKDIR /src

# Copy the file to the working directory
COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Command add is the source we want to add followed by the destionation, which is the current directory /src in this case
COPY src/ .

CMD ["python", "telegram-interface.py"]