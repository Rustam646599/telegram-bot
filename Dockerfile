FROM python:3.8-slim-buster
WORKDIR /telegram-bot
COPY requirements.txt /telegram-bot/requirements.txt
RUN pip install -r /telegram-bot/requirements.txt
COPY . .
CMD ["python", "bot.py"]
