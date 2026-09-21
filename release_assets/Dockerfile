# Reproduces the environment the paper was built in.
#
#   docker build -t labor-backing .
#   docker run --rm -v "$PWD:/pkg" labor-backing make headline
FROM python:3.12.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pkg
COPY requirements.lock /tmp/requirements.lock
RUN pip install --no-cache-dir -r /tmp/requirements.lock

ENV PYTHONHASHSEED=0
CMD ["make", "headline"]
