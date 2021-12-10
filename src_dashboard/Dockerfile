FROM python:3.8-slim-buster
LABEL maintainer="bgokbakan@gmail.com"

COPY assets assets
COPY apps apps
COPY components components
COPY utils utils


COPY app.py .
COPY index.py .

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install pyarrow

#CMD ["python", "index.py"]
CMD gunicorn --workers=1 --threads=4 --worker-class=gthread --bind 0.0.0.0:8050 index:server