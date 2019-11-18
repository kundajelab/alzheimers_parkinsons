FROM tensorflow/tensorflow:1.14.0-gpu-py3
RUN apt-get -y update
RUN apt-get -y upgrade --fix-missing
RUN pip install keras==2.2.4
RUN apt-get install -y git
RUN apt-get install libcurl4 libcurl4-openssl-dev -y
RUN pip install pyBigWig 
WORKDIR /root
RUN git clone https://github.com/kundajelab/kerasAC.git
WORKDIR kerasAC
RUN python setup.py build
RUN python setup.py develop
WORKDIR /root
RUN git clone https://github.com/kundajelab/alzheimers_parkinsons.git
WORKDIR alzheimers_parkinsons/nautilus_cv_pseudobulk
RUN chmod +x *sh
