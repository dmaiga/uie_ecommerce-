ARG RANGER_VERSION=2.4.0
ARG RANGER_DB_TYPE=postgres
ARG RANGER_ADMIN_JAVA_VERSION=11
ARG TARGETARCH=amd64

FROM ubuntu:22.04 as base
ENV DEBIAN_FRONTEND=noninteractive

# Java, Python, tools
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget tar python3 python3-pip curl netcat unzip gnupg && \
    apt-get clean


ENV JAVA_HOME=/usr/lib/jvm/java-1.${RANGER_ADMIN_JAVA_VERSION}.0-openjdk-${TARGETARCH}
ENV PATH=$PATH:$JAVA_HOME/bin
ENV RANGER_HOME=/opt/ranger
ENV RANGER_SCRIPTS=/home/ranger/scripts

RUN useradd -ms /bin/bash ranger

# Préparation des dossiers
RUN mkdir -p ${RANGER_HOME} ${RANGER_SCRIPTS} /var/run/ranger /var/log/ranger /usr/share/java \
    && chown -R ranger:ranger ${RANGER_HOME} ${RANGER_SCRIPTS} /var/run/ranger /var/log/ranger

# Téléchargement Ranger
WORKDIR /home/ranger
RUN wget https://downloads.apache.org/ranger/${RANGER_VERSION}/ranger-${RANGER_VERSION}-admin.tar.gz

# Décompression et installation
RUN tar xvf ranger-${RANGER_VERSION}-admin.tar.gz -C ${RANGER_HOME} && \
    ln -s ${RANGER_HOME}/ranger-${RANGER_VERSION}-admin ${RANGER_HOME}/admin && \
    rm ranger-${RANGER_VERSION}-admin.tar.gz

# Configuration et scripts
COPY ranger-admin-install-postgres.properties ${RANGER_HOME}/admin/install.properties
COPY entrypoint.sh ${RANGER_SCRIPTS}/ranger.sh
COPY downloads/postgresql-42.7.6.jar /usr/share/java/postgresql.jar
COPY create-ranger-services.py ${RANGER_SCRIPTS}/

RUN chmod +x ${RANGER_SCRIPTS}/ranger.sh && chown -R ranger:ranger ${RANGER_SCRIPTS}

USER ranger
ENTRYPOINT ["/home/ranger/scripts/ranger.sh"]
