FROM apache/airflow:slim-2.10.5-python3.11

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev

USER airflow
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install -r /opt/airflow/requirements.txt