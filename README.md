watershed.py
============

Delineate watersheds upstream of a given point. Based on [HydroSHEDS 30as](http://hydrosheds.org). Built on [rasterio](http://github.com/mapbox/rasterio) and [GDAL](http://gdal.org).

#Usage

```
import watershed

loc = (-80,41)      # long,lat
snap_distance = 0.5 # decimal degrees
outfile = 'my_watershed.shp'

snapped_loc = watershed.snap_to_point(loc, snap_distance)
watershed.delineate_watershed(snapped_loc, outfile)

# delineates a watershed and saves it as 'my_watershed.shp'
```

The file format exported by ```watershed.delineate_watershed``` is determined by the output file extension, which must be one of:
- ```.json``` for json
- ```.shp``` for shapefile
- ```.zip``` for zipped shapefile
- ```.tif``` for binary geotiff

#Install
Watersheds.py requires numpy headers to build. After install download and extract the preprocessed [flow direction data](http://md.cc.s3.amazonaws.com/tmp/assets.7z) (large file).

```
pip install -r http://raw.github.com/fgassert/watershed.py/master/requirements.txt
pip install git+http://raw.github.com/fgassert/watershed.py.git
```

Download and extract the flow direction data to your project directory

```
cd YOUR_PROJECT
wget http://md.cc.s3.amazonaws.com/tmp/assets.7z
p7zip -d assets.7z
```

#License
Source: (c) 2014 Francis Gassert [MIT](http://opensource.org/licenses/MIT)

##HydroSHEDS

This product incorporates data from the HydroSHEDS database which is © World Wildlife Fund, Inc. (2006-2013) and has been used herein under license. WWF has not evaluated the data as altered and incorporated within, and therefore gives no warranty regarding its accuracy, completeness, currency or suitability for any particular purpose. Portions of the HydroSHEDS database incorporate data which are the intellectual property rights of © USGS (2006-2008), NASA (2000-2005), ESRI (1992-1998), CIAT (2004-2006), UNEP-WCMC (1993), WWF (2004), Commonwealth of Australia (2007), and Her Royal Majesty and the British Crown and are used under license. The HydroSHEDS database and more information are available at http://www.hydrosheds.org.

