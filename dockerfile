FROM ubuntu:noble

WORKDIR /opt
COPY src/ .
COPY requirements.txt .

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt-get update
RUN apt-get install -y python3.12 python3-pip python3-venv
RUN bash /opt/generate_certs.sh
RUN python3.12 -m venv venv

ENV PATH="/opt/venv/bin:$PATH"


RUN python3 -m pip install -r requirements.txt

EXPOSE 443
CMD python3 deviceCheckout.py
# ENTRYPOINT ["python3", "deviceCheckout.py"]

