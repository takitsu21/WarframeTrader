FROM python:alpine
LABEL Name=warframetrader-v0.0.2 Version=0.0.1
WORKDIR /app
COPY . /app

RUN python3.7 -m pip install -r requirements.txt
CMD ["python3.7", "-m", "warframetrader-v0.0.2"]