FROM pypy:3

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN mkdir /code
RUN chown nobody /code

USER nobody

RUN git clone https://github.com/cnorthwood/adventofcode.git /code
CMD /entrypoint.sh
