FROM ubuntu
LABEL maintainer="Lucas Alves Martins"
ENV container=docker

COPY ./data /data/
RUN apt-get -y update \
 && apt-get -y install \
      sudo\
      wget\
      unzip\
      nano\
      jq\
      git\
      python\
      libmysqlclient-dev\
      python-dev \
      python-pip\
 && pip install -r /data/requirements.txt


EXPOSE 8000
ENTRYPOINT ["/data/web/init.sh"]

CMD ["/bin/bash"]
CMD ["/usr/sbin/init"]
