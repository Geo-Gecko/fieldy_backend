# FROM mdillon/postgis
# RUN apt-get update

FROM osgeo/gdal:ubuntu-small-latest

RUN mkdir app


# Add the application source code.
ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
  apt-utils\
  binutils \
  build-essential\
  python3-dev \
  python3-distutils\
  libpq-dev

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py

RUN pip install psycopg2-binary
RUN pip install gunicorn



# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
# ADD requirements_copy.txt /app/requirements_copy.txt
RUN pip install -r /app/requirements.txt

# RUN python manage.py migrate
# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
CMD gunicorn -b 0.0.0.0:$PORT sh_backend.wsgi