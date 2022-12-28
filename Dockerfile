FROM ubuntu
MAINTAINER pablo@caldito.me
RUN apt update && apt install -y curl
COPY ipwarn /usr/local/bin/
RUN mkdir /etc/ipwarn
COPY config/ipwarn.conf /etc/ipwarn/ipwarn.conf
CMD ["/usr/local/bin/ipwarn"]
