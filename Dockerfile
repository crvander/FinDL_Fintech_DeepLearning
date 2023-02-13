ARG BASE_CONTAINER=ucsdets/datahub-base-notebook:2022.3-stable

FROM $BASE_CONTAINER

LABEL maintainer="UC San Diego ITS/ETS <ets-consult@ucsd.edu>"
COPY requirements.txt ./

USER root

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/bin/bash"]
