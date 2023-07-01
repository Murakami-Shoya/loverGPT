FROM nvidia/cuda:11.7.1-base-ubuntu22.04

USER root

COPY ./requirements.txt /tmp
WORKDIR /code

RUN apt-get update && apt-get -y upgrade
# cv2のためlibgl1-mesa-devをインストール
# RUN apt-get install -y libopencv-dev
RUN apt install git -y
RUN apt install -y curl python3 python3-distutils
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
# RUN pip install ez_setup
RUN pip install -Uqq git+https://github.com/huggingface/peft.git
RUN pip install -r /tmp/requirements.txt
# RUN pip3 install -U torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# docker run -it --rm --gpus all -v `pwd`/src:/code -p 8888:8888 --shm-size=8g --name my-jupyter ml_cuda_env sh -c 'jupyter-lab --allow-root --ip=*'