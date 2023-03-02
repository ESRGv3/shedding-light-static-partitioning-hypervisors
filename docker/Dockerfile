FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

ARG AARCH64_TOOLCHAIN_LINK=https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-x86_64-aarch64-none-elf.tar.xz
ARG AARCH64_LINUX_TOOLCHAIN_LINK=https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-x86_64-aarch64-none-linux-gnu.tar.xz

RUN apt-get update && apt-get install -y \
        git \
        build-essential \
        gcc-multilib \
        curl \
        xz-utils

RUN mkdir /opt/aarch64-toolchain && curl $AARCH64_TOOLCHAIN_LINK | tar xJ -C /opt/aarch64-toolchain --strip-components=1
RUN mkdir /opt/aarch64-linux-toolchain && curl $AARCH64_LINUX_TOOLCHAIN_LINK | tar xJ -C /opt/aarch64-linux-toolchain --strip-components=1
ENV PATH=$PATH:/opt/aarch64-toolchain/bin:/opt/aarch64-linux-toolchain/bin

RUN apt-get update && apt-get install -y \
        libncurses-dev \
        file \
        wget \ 
        cpio \
        unzip \
        rsync \
        bc \
        flex \
        bison \
        libssl-dev \
        libelf-dev \
        kmod \
        device-tree-compiler \
        u-boot-tools \
        cloc

RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \  
    apt-get update && apt-get install -y python3.9 python3.9-distutils && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.9 get-pip.py

RUN apt-get install -y cmake ccache ninja-build cmake-curses-gui \
        libxml2-utils ncurses-dev doxygen protobuf-compiler python3-protobuf \
        clang libssl-dev libclang-dev libcunit1-dev libsqlite3-dev \
        haskell-stack && stack upgrade --binary-only
RUN pip install mako pyelftools pyfdt jinja2 plyplus future aenum bs4 guardonce cmake-format==0.4.5 \
        six pyaml pexpect jsonschema autopep8==1.4.3 lxml libarchive-c sh psutil \
        PyYAML beautifulsoup4 persistent ptyprocess concurrencytest fixtures sortedcontainers \
        extras pycparser pbr ordered-set exceptiongroup hypothesis testtools python-subunit

RUN addgroup user && adduser -disabled-password --ingroup user user
USER user
RUN git config --global user.email "user@example.com" && git config --global user.name "User"

CMD /bin/bash
