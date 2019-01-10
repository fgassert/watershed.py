from . import _watershed
import rasterio
import fiona
import numpy as np
import os
import zipfile
from rasterio.features import shapes

ASSETS = "assets"
SNAP_RAS = os.path.join(ASSETS,"gl_acc_30s.tif")
REGION_RAS = os.path.join(ASSETS,"region_id.tif")

def delineate_watershed(pt, o):
    """ delineates a watershed and writes it to file based on extension """
    with rasterio.open(REGION_RAS) as src:
        x,y = from_longlat(pt, src.transform)
        region = src.read(1, window=((x,x+1),(y,y+1)))[0,0]

    if region < 1:
        print ("ERROR: point out of bounds")
        return None

    fd_ras = os.path.join(ASSETS,"dir_0%d.tif" % region)
    with rasterio.open(fd_ras) as src:
        x,y = from_longlat(pt, src.transform)
        dat = src.read(1)

    res = _watershed.watershed_from_d8(int(x),int(y),dat)

    ext = os.path.splitext(o)[1]

    if ext == '.tif':
        meta = src.meta
        meta.update({'driver':'GTiff',
                     'dtype':rasterio.ubyte,
                     'compress':'lzw'})
        with rasterio.open(o,'w',**meta) as dst:
            dst.write_band(1,res)

    if ext in ('.zip', '.shp', '.json', '.geojson'):
        poly = [
            {'properties':{'pour_lat':pt[1],'pour_long':pt[0]},'geometry':s}
            for s,v in shapes(res,
                           mask=res>0,
                           transform=src.transform,
                           connectivity=8)][0]
        schema = {'properties':[('pour_lat','float'),
                                ('pour_long','float')],
                  'geometry':'Polygon'}
        if ext == '.zip':
            with fiona.open(o[:-4]+'.shp','w',
                            'ESRI Shapefile',
                            crs=src.crs,
                            schema=schema) as dst:
                dst.write(poly)
            with zipfile.ZipFile(o,'w') as z:
                for e in ['.shp','.shx','.dbf','.cpg','.prj']:
                    z.write(o[:-4]+e, arcname=os.path.basename(o[:-4]+e))
                    os.remove(o[:-4]+e)
        elif ext == '.shp':
            with fiona.open(o,'w',
                            'ESRI Shapefile',
                            crs=src.crs,
                            schema=schema) as dst:
                dst.write(poly)
        elif ext == '.json' or ext == '.geojson':
            if os.path.isfile(o):
                os.remove(o)
            with fiona.open(o,'w',
                            'GeoJSON',
                            crs=src.crs,
                            schema=schema) as dst:
                dst.write(poly)
    else:
        raise Exception("Cound not parse file format.")

def snap_to_highest(pt, d, r=None):
    """ snap point to highest point within d degrees in raster r """
    if r is None:
        r = SNAP_RAS
    with rasterio.open(r) as src:
        x,y = from_longlat(pt, src.transform)
        d = d/abs(src.res[0])
        minx = max(x-d,0)
        maxx = min(x+d+1,src.shape[0])
        miny = max(y-d,0)
        maxy = min(y+d+1,src.shape[1])
        crop = src.read(1,window=((minx,maxx),(miny,maxy)))
        idx = np.argmax(crop)
        x2,y2 = np.unravel_index(idx, crop.shape)
        pt = to_longlat((minx+x2, miny+y2), src.transform)
    return pt

def from_longlat(pt, affine):
    y,x = ~affine*(pt)
    return x,y

def to_longlat(pt, affine):
    return affine*(pt[1],pt[0])
