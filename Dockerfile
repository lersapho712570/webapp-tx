FROM centos:centos7

RUN yum update -y && yum install -y python3

RUN mkdir /opt/webapp && mkdir /tmp/data

COPY . /opt/webapp

RUN pip3 install -r /opt/webapp/requirements.txt

ENTRYPOINT cd /opt/webapp && python3 webapp_write.py
