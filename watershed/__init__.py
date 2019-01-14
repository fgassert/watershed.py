from . import _watershed
import rasterio
import fiona
import numpy as np
import os
import zipfile
import logging
from rasterio.features import shapes

ASSETS = "assets"
SNAP_RAS = os.path.join(ASSETS,"gl_acc_30s.tif")
REGION_RAS = os.path.join(ASSETS,"region_id.tif")
logging.basicConfig(level=logging.INFO)

def delineate_watershed(pt, o, snap=0):
    f = os.path.splitext(o)[1]
    if snap > 0:
        pt = snap_to_highest(pt, snap)

    with rasterio.open(REGION_RAS) as src:
        x, y = from_latlong(pt[0], pt[1], src.transform)
        region = src.read(1, window=((y, y+1), (x, x+1)))[0,0]

    if region < 1:
        raise Exception("Point out of bounds (no region)")

    fd_ras = os.path.join(ASSETS,"dir_0%d.tif" % region)
    with rasterio.open(fd_ras) as src:
        x, y = from_latlong(pt[0], pt[1], src.transform)
        dat = src.read(1)

    res = _watershed.watershed_from_d8(int(y), int(x), dat)

    if f == '.tif':
        meta = src.meta
        meta.update({'driver':'GTiff',
                     'dtype':rasterio.ubyte,
                     'compress':'lzw'})
        with rasterio.open(o,'w',**meta) as dst:
            dst.write_band(1, res)

    elif f in ('.zip', '.shp', '.json', '.geojson'):
        poly = [
            {'properties':{'pour_lat':pt[0],'pour_long':pt[1]},'geometry':s}
            for s,v in shapes(res,
                           mask=res>0,
                           transform=src.transform,
                           connectivity=8)][0]
        schema = {'properties':[('pour_lat','float'),
                                ('pour_long','float')],
                  'geometry':'Polygon'}

        if f == '.zip':
            with fiona.open(o[:-4]+'.shp','w',
                            'ESRI Shapefile',
                            crs=src.crs,
                            schema=schema) as dst:
                dst.write(poly)
            with zipfile.ZipFile(o, 'w') as z:
                for e in ['.shp','.shx','.dbf','.cpg','.prj']:
                    z.write(o[:-4]+e, arcname=os.path.basename(o[:-4]+e))
                    os.remove(o[:-4]+e)

        elif f == '.shp':
            with fiona.open(o,'w',
                            'ESRI Shapefile',
                            crs=src.crs,
                            schema=schema) as dst:
                dst.write(poly)

        elif f == '.json' or f == '.geojson':
            if os.path.isfile(o):
                os.remove(o)
            with fiona.open(o,'w',
                            'GeoJSON',
                            crs=src.crs,
                            schema=schema) as dst:
                dst.write(poly)
    else:
        raise Exception("Cound not parse file format.")
    return o

def snap_to_highest(pt, d, r=None):
    """ snap point to highest point within d degrees in raster r """
    if r is None:
        r = SNAP_RAS
    with rasterio.open(r) as src:
        x, y = from_latlong(pt[0], pt[1], src.transform)
        logging.info(src.transform)
        logging.info(src.meta)
        logging.info((x, y))
        d = d/abs(src.res[0])
        miny = max(y-d, 0)
        maxy = min(y+d+1, src.shape[0])
        minx = max(x-d, 0)
        maxx = min(x+d+1, src.shape[1])
        crop = src.read(1, window=((miny, maxy), (minx, maxx)))
        logging.info(crop)
        if len(crop) < 1:
            raise Exception("Point out of bounds (no snap)")
        idx = np.argmax(crop)
        logging.info(idx)
        y2, x2 = np.unravel_index(idx, crop.shape)
        pt = to_latlong(minx+x2, miny+y2, src.transform)
        logging.info(pt)
    return pt

def from_latlong(lat, lng, affine):
    return (lng, lat) * ~affine

def to_latlong(col, row, affine):
    lng, lat = affine * (col, row)
    return lat, lng
