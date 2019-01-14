FROM python:3

RUN apt-get update
RUN pip install --upgrade pip

RUN apt-get install -y gdal-bin libgdal-dev p7zip
RUN pip install cython numpy rasterio fiona

RUN wget http://md.cc.s3.amazonaws.com/tmp/assets.7z
RUN p7zip -d assets.7z

COPY . .
RUN python setup.py build_ext --inplace
RUN python setup.py install

CMD python watershed/test.py
