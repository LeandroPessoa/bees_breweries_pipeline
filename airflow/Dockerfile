# The requested changes are for the docker-compose.yaml file and do not affect the Dockerfile provided.
# Therefore, no changes are made to this Dockerfile.
FROM apache/airflow:2.8.1

USER root
RUN apt-get update && apt-get install -y gcc
RUN apt-get update && apt-get install -y openjdk-17-jre-headless
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN pip install --no-cache-dir boto3 s3fs

# Baixar os JARs do hadoop-aws e aws-java-sdk-bundle
USER root
RUN mkdir -p /opt/airflow/jars && \
    curl -o /opt/airflow/jars/hadoop-aws-3.3.2.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar && \
    curl -o /opt/airflow/jars/aws-java-sdk-bundle-1.11.1026.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar

USER airflow

