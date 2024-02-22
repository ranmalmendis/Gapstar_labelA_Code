FROM python:3.10
LABEL author='Label A'

WORKDIR /app

# Environment setup and package installation
RUN apt-get update && \
    apt-get install -y bash vim nano postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install major dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir flake8==3.8.4 uWSGI

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the codebase into the container
COPY . .

# Ensure manage.py is executable
RUN chmod +x manage.py

# Collect static files
RUN ./manage.py collectstatic --noinput

# Operational parameters
ENV WORKERS=2
ENV PORT=8000  
ENV PYTHONUNBUFFERED=1
ENV UWSGI_HTTP=0.0.0.0:${PORT}
ENV UWSGI_WSGI_FILE=autocompany/wsgi.py
ENV UWSGI_MASTER=1
ENV UWSGI_WORKERS=${WORKERS}
ENV UWSGI_THREADS=2  
ENV UWSGI_STATIC_MAP="/static=/static"

EXPOSE ${PORT}

# Command to start uWSGI
CMD ["uwsgi", "--http", "${UWSGI_HTTP}", "--module", "${UWSGI_WSGI_FILE}", "--master", "--processes", "${UWSGI_WORKERS}", "--threads", "${UWSGI_THREADS}", "--static-map", "${UWSGI_STATIC_MAP}"]
