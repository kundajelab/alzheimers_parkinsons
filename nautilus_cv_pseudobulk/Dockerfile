FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
RUN set -x \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends \
        redis-tools \
        netcat \
        net-tools \
        openssh-client \
        openconnect \
        openvpn \
        wget \
        bzip2 \
        ca-certificates \
        sudo \
        locales \
        fonts-liberation \
        build-essential \
        emacs \
        git \
        inkscape \
        jed \
        libsm6 \
        libxext-dev \
        libxrender1 \
        lmodern \
        pandoc \
        python-dev \      
        vim \
        curl \
        wget \
        unzip \
        gdal-bin libgdal-dev python3-gdal
RUN apt install -y python3-pip
RUN rm /usr/bin/python
RUN ln -s /usr/bin/python3.6 /usr/bin/python
#RUN rm /usr/bin/pip
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip install \
        argparse \
        imutils \
        keras==2.2.4 \
        nbgitpuller \
        opencv-python \
        requests \
        tensorflow-gpu==1.14.0 \
        torch \
        torchvision \
        visualdl==1.3.0 \
        git+https://github.com/veeresht/CommPy.git \
        tensorflow-probability \
        bash_kernel \
        matlab_kernel \
        pygdal==2.2.3.3
USER root 
RUN apt-get install -y libbz2-dev liblzma-dev
RUN apt-get install -y git
RUN apt-get install libcurl4 libcurl4-openssl-dev -y
RUN pip install pyBigWig
RUN pip install pysam
RUN pip install tables 
RUN pip install tiledb 
RUN pip install psutil 

WORKDIR /root
RUN git clone https://github.com/kundajelab/kerasAC.git
WORKDIR kerasAC
RUN python setup.py build
RUN python setup.py develop
WORKDIR /root
RUN git clone https://github.com/kundajelab/alzheimers_parkinsons.git
WORKDIR alzheimers_parkinsons/nautilus_cv_pseudobulk
RUN git pull
RUN chmod +x *sh
