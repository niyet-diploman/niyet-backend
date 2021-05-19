# Build from python image.
FROM python:3.8

RUN : "---------- install be build container deps ----------" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        openssh-client \
        build-essential \
        make \
        gcc \
        xmlsec1 \
        gettext \
        # TODO: remove when py38 wheel for pylibmc is available
        libmemcached-dev \
        zlib1g-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Set python requirements
WORKDIR /code

# Install python dependencies
COPY ./requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set volume for database and static files.
RUN mkdir -p /static /media

# Copy source code
COPY . /code
#RUN cp .env.example .env
# Collect static
#RUN python manage.py collectstatic --noinput

CMD ["./bin/docker-entrypoint.sh"]
