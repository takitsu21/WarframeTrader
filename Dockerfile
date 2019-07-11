FROM python:3.7.3
WORKDIR /app
COPY requirements.txt /app/
COPY . /app
RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "main.py" ]