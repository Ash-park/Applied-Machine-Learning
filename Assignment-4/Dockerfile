FROM python:3.13-slim

COPY Assignment-4/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY Assignment-1 /Assignment-1
COPY Assignment-2 /Assignment-2
COPY Assignment-3 /Assignment-3

WORKDIR /Assignment-3

ENTRYPOINT ["python"]
CMD ["app.py"]
