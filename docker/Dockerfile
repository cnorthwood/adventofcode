FROM fedora:43

RUN dnf install -y python3 python3-pip pypy3 nodejs python3-shapely python3-scipy python3-numpy && pypy3 -mensurepip && pypy3 -mpip install z3-solver

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD /entrypoint.sh
