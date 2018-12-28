FROM pypy:3

RUN pypy3 -mpip install z3-solver

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nobody

CMD /entrypoint.sh
