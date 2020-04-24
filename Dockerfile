FROM python:3.7.7-alpine

WORKDIR sa-tools-core
COPY . /sa-tools-core
RUN set -ex \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache gcc python3-dev musl-dev libffi-dev openssl-dev ncdu \
    && python -m pip install --index-url https://pypi.doubanio.com/simple --no-cache-dir .[script,icinga,tencentcloud] \
    && apk del gcc python3-dev musl-dev libffi-dev openssl-dev \
    && mkdir -p /etc/sa-tools/config.py \
    && cp -rfv ./local_config.py.example /etc/sa-tools/ \
    && mv -v /etc/sa-tools/local_config.py.example /etc/sa-tools/config.py \
    && cp -rfv ./examples/config /etc/sa-tools/ \
    && rm -rfv ./*

VOLUME ["/etc/sa-tools/", "/etc/sa-tools-config/", "/usage-path", "/ncdu-data-path"]