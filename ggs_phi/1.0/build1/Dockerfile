FROM ubuntu_messaging_python3:18.04-build1
MAINTAINER Lars Zimmer <lars.zimmer@trevisto.de>

# configure pip
RUN pip3 install \
    rasterio \
    matplotlib

# copy sources
COPY phi.py /start.py

