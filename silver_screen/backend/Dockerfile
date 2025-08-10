FROM python:3.10

WORKDIR /opt/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'


COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

RUN apt-get update && apt-get install -y gettext && apt install -y ncat

# RUN apt update && apt-get install netcat
# apt install -y netcat
RUN pip install --upgrade pip

ENV TZ=America/Toronto
RUN apt install tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt \
     && pip install -r requirements-dev.txt     

COPY . .

EXPOSE 8000

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]