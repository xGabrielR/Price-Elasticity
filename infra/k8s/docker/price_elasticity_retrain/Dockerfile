FROM python:3.11.0

WORKDIR /app
COPY /requirements.txt /requirements.txt
COPY /main.py /main.py

RUN pip install -r /requirements.txt

CMD python /main.py