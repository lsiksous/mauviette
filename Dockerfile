# Dockerfile
FROM python:3.10

RUN apt-get update && apt-get -y install

# Upgrade pip and setuptools
RUN pip install --upgrade pip && \
    pip install -U setuptools

WORKDIR /app

COPY requirements.txt .
COPY src src
COPY notebooks notebooks

RUN pip install -r requirements.txt

EXPOSE 8888
ENTRYPOINT ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root","--NotebookApp.token=''","--NotebookApp.password=''"]