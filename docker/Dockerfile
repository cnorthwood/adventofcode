FROM fedora:41

RUN dnf install -y python3 python3-pip pypy3 nodejs && pypy3 -mensurepip && pypy3 -mpip install z3-solver

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD /entrypoint.sh
