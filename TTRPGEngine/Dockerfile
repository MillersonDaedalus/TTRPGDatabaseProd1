FROM python:3.12
LABEL authors="tmills"

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app
COPY . /app

# Verify required files exist

# Stop default Apache (mod_wsgi-express starts its own)
RUN service apache2 stop

RUN test -f mod_wsgi-express || (echo "Missing wsgi.py" && exit 1)


EXPOSE 80
CMD ["/usr/bin/mod_wsgi-express", "start-server", "TTRPGEngine/wsgi.py", "--port=80", "--user=www-data", "--group=www-data"]