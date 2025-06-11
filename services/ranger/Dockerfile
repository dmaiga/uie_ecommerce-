# services/ranger/Dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV RANGER_VERSION=2.3.0
ENV RANGER_BASE=/opt
ENV RANGER_DIR=apache-ranger-${RANGER_VERSION}-admin
ENV RANGER_HOME=${RANGER_BASE}/${RANGER_DIR}
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    openjdk-8-jdk \
    wget \
    mysql-client \
    python3 \
    netcat \
    unzip \
    libmysql-java && \
    ln -s /usr/share/java/mysql-connector-java.jar /usr/lib/mysql-connector-java.jar && \
    apt-get clean

# Download and extract Apache Ranger Admin from archive
RUN wget https://archive.apache.org/dist/ranger/${RANGER_VERSION}/${RANGER_DIR}.tar.gz && \
    tar -xzf ${RANGER_DIR}.tar.gz -C ${RANGER_BASE} && \
    rm ${RANGER_DIR}.tar.gz

# Copy config files
COPY conf/install.properties ${RANGER_HOME}/install.properties
COPY conf/ranger-admin-site.xml ${RANGER_HOME}/templates/ranger-admin-site.xml

# Setup Ranger
WORKDIR ${RANGER_HOME}
RUN chmod +x setup.sh && ./setup.sh

EXPOSE 6080

CMD ["sh", "-c", "${RANGER_HOME}/ews/start-ranger-admin.sh && tail -f /dev/null"]
