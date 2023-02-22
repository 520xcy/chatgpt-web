FROM alpine:latest

# environment
ENV MIRROR=http://mirrors.cloud.tencent.com/alpine
ENV PACKAGES=alpine-baselayout,\
alpine-keys,\
apk-tools,\
busybox,\
libc-utils,\
xz

ENV OPENAI_API_KEY=

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories && \
apk update && \
apk add --no-cache \
shadow \
gcc \
g++ \
python3-dev \
python3 && \
python3 -m ensurepip && \
pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple revChatGPT flask flask_cors && \
apk del --purge \
python3-dev \
g++ \
gcc && \
rm -rf /root/.cache /tmp/* && \
echo "**** create abc user and make our folders ****" && \
groupmod -g 1000 users && \
useradd -u 911 -U -d /workdir -s /bin/sh abc && \
usermod -G users abc && \
mkdir -p /workdir

COPY shell/init.sh /

COPY chatgetweb/ /workdir

VOLUME /workdir/output

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "/init.sh"]
