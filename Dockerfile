FROM python:3.7-slim
RUN apt-get update && apt-get install -y gcc
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app/
RUN python3 -m pytest tests
ENTRYPOINT ["python3", "-m"]
CMD ["app"]