FROM ubuntu:18.04

ARG PACKAGE=intel-openvino-dev-ubuntu18-2020.3.194

RUN apt-get update && apt-get -y upgrade

RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    wget \
    build-essential \
    apt-utils \
    python3.6 \
    libpython3.6 \
    python3-pip \
    python3-setuptools \
    cmake \
    sudo  \
    libgtk-3-dev

RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev

RUN wget https://apt.repos.intel.com/openvino/2020/GPG-PUB-KEY-INTEL-OPENVINO-2020 && \
  apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2020

RUN echo "deb https://apt.repos.intel.com/openvino/2020 all main" > /etc/apt/sources.list.d/intel-openvino-2020.list

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    $PACKAGE && \
  apt autoremove -y && \
  rm -rf /var/lib/apt/lists/*


COPY common app/src/person_detection_retail_0013/common/
COPY config.py app/src/person_detection_retail_0013/
COPY models/person-detection-retail-0013/ app/models/person-detection-retail-0013/
COPY src/person_detection_retail_0013/ app/src/person_detection_retail_0013/

RUN pip3 install -r app/src/person_detection_retail_0013/requirements.txt

WORKDIR app/

ENTRYPOINT ["bash", "src/person_detection_retail_0013/run.sh"]
