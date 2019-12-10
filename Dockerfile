# Nobrainer container specification.
# Use "gpu-py3" to build GPU-enabled container and "py3" for non-GPU container.
ARG TF_ENV="gpu-py3"
FROM tensorflow/tensorflow:2.0.0-gpu-py3
WORKDIR /opt/nobrainer
COPY . .
RUN apt-get update -qq \
    && apt-get install -yq --no-install-recommends imagemagick \
    && apt-get install -y nodejs \
    && apt-get install -y npm \
    && apt-get clean \
    && pip3 install --upgrade pip \ 
    && pip3 install --no-cache-dir \
        scikit-image \  
        ipython \
        jupyterlab \
	pygame \
	numpy \
        seaborn \
        opencv-python \
        floodfill \
        ipympl \
        pillow \
        numba \
        gym \
        torch \
        torchvision \
        tensorboardx \
        requests \
    && apt-get install -yq locales \
    && export LC_ALL="en_US.UTF-8" \
    && export LC_CTYPE="en_US.UTF-8" \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build \
    && jupyter labextension install jupyter-matplotlib \
    && dpkg-reconfigure locales \
    && apt update && apt install -y libsm6 libxext6 libxrender-dev \ 
    && rm -rf ~/.cache/pip/* \
    && useradd --no-user-group --create-home --shell /bin/bash neuro 
ENV PATH="$PATH:/opt/nobrainer/bin"
USER neuro
WORKDIR /home/neuro

