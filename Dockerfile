FROM python:3.9

WORKDIR /demo
ADD requirements.txt .
RUN pip install --pre -r requirements.txt --find-links=https://s3.amazonaws.com/pypi.datadoghq.com/trace-dev/index.html

COPY . .

ENTRYPOINT pytest
CMD [--ddtrace, -vvv, --record-mode=none]

