FROM seleniarm/standalone-chromium:latest

RUN sudo apt-get update -y && sudo apt-get install -y python3 python3-pip 
RUN sudo ln -s /bin/python3 /bin/python
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt
COPY app /app

ENV PATH="/home/seluser/.local/bin:${PATH}"
WORKDIR /