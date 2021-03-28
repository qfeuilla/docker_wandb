FROM python:3.6-stretch
MAINTAINER Quentin FEUILLADE--MONTIXI <quentin.feuillade33@gmail.com>

# install build utilities
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential

# check our python environment
RUN python3 --version
RUN pip3 --version

# set the working directory for containers
WORKDIR  /usr/src/wandb_lab

# Installing python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade -r requirements.txt

# Copy all the files from the project’s root to the working directory
COPY src/ /src/
COPY entrypoint.sh entrypoint.sh
RUN ls -la /src/*

CMD ["sh", "entrypoint.sh"]
