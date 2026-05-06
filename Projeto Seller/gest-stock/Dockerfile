FROM python:3.11.15
WORKDIR /src
COPY requirements.txt requirements.txt

RUN apt update && apt install -y netcat-traditional
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["bash", "-c", "echo 'Aguardando MySQL...' && while ! nc -z db 3306; do sleep 1; done && echo 'MySQL pronto!' && flask db upgrade && python run.py"]