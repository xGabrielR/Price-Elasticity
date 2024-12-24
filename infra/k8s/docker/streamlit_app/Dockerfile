FROM python:3.11.0

# ENV MLFLOW_TRACKING_SERVER=${MLFLOW_TRACKING_SERVER}

WORKDIR /app
COPY /requirements.txt /requirements.txt
COPY /main.py /main.py

RUN pip install -r /requirements.txt

CMD streamlit run /main.py