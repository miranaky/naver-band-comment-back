FROM python:3.11

RUN apt update -y && apt install wget libgl1-mesa-glx libxss1 libappindicator1 chromium chromium-driver chromium-sandbox  -y
# RUN apt-get update && apt-get install -y libglib2.0-0 libnss3 libxcb1 wget unzip
# RUN apt-get install -y chromium-common=12.0.5615.49-0ubuntu0.18.04.1 chromium-sandbox
# RUN apt-get install -y chromium=112.0.5615.49-0ubuntu0.18.04.1 chromium-driver=112.0.5615.49-0ubuntu0.18.04.1
# RUN cp /usr/bin/chromedriver /usr/local/bin/

# RUN apt-get update && \
#     apt-get install -y firefox-esr && \
#     wget -q https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
#     tar -xzf /tmp/geckodriver.tar.gz -C /opt && \
#     rm /tmp/geckodriver.tar.gz && \
#     chmod 755 /opt/geckodriver && \
#     ln -fs /opt/geckodriver /usr/bin/geckodriver && \
#     ln -fs /opt/geckodriver /usr/local/bin/geckodriver

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt
COPY app /app

WORKDIR /