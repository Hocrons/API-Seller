FROM python:3.11.15
WORKDIR /src
COPY requirements.txt requirements.txt

RUN apt update && apt install -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "run.py"]