import watershed._watershed
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
    with rasterio.drivers():
        with rasterio.open(REGION_RAS) as src:
            x,y = from_longlat(pt,src.affine)
            region = src.read_band(1, window=((x,x+1),(y,y+1)))[0,0]
        
        if region < 1:
            print "ERROR: point out of bounds"
            return None

        fd_ras = os.path.join(ASSETS,"dir_0%d.tif" % region)
        with rasterio.open(fd_ras) as src:
            x,y = from_longlat(pt,src.affine)
            dat = src.read_band(1)
        
    res = _watershed.watershed_from_d8(int(x),int(y),dat)

    ext = os.path.splitext(o)[1]
    
    if ext == '.tif':
        with rasterio.drivers():
            meta = src.meta
            meta.update({'driver':'GTiff',
                         'dtype':rasterio.ubyte,
                         'compress':'lzw'})
            with rasterio.open(o,'w',**meta) as dst:
                dst.write_band(1,res)

    if ext in ('.zip', '.shp', '.json'):
        polys = (
            {'properties':{'pour_lat':pt[1],'pour_long':pt[0]},'geometry':s}
            for s,v in shapes(res, 
                           mask=res>0, 
                           transform=src.affine, 
                           connectivity=8))
        schema = {'properties':[('pour_lat','float'),
                                ('pour_long','float')],
                  'geometry':'Polygon'}
        with fiona.drivers():
            if ext == '.zip':
                """
                o_shp = os.path.basename(o[:-4])+'.shp'
                with fiona.open(o_shp,'w',
                                'ESRI Shapefile',
                                vfs='zip://./%s/' % o,
                                crs=src.crs,
                                schema=schema) as dst:
                    dst.writerecords(polys)
                """
                with fiona.open(o[:-4]+'.shp','w',
                                'ESRI Shapefile',
                                crs=src.crs,
                                schema=schema) as dst:
                    dst.writerecords(polys)
                with zipfile.ZipFile(o,'w') as z:
                    for e in ['.shp','.shx','.dbf','.cpg','.prj']:
                        z.write(o[:-4]+e, arcname=os.path.basename(o[:-4]+e))
                        os.remove(o[:-4]+e)
            elif ext == '.shp':
                with fiona.open(o,'w',
                                'ESRI Shapefile',
                                crs=src.crs,
                                schema=schema) as dst:
                    dst.writerecords(polys)
            if ext == '.json':
                if os.path.isfile(o):
                    os.remove(o)
                with fiona.open(o,'w',
                                'GeoJSON',
                                crs=src.crs,
                                schema=schema) as dst:
                    dst.writerecords(polys)
            

def snap_to_highest(pt, d, r=None):
    """ snap point to highest point within d degrees in raster r """
    if r is None:
        r = SNAP_RAS
    with rasterio.drivers():
        with rasterio.open(r) as src:
            x,y = from_longlat(pt, src.affine)
            d = d/abs(src.res[0])
            minx = max(x-d,0)
            maxx = min(x+d+1,src.shape[0])
            miny = max(y-d,0)
            maxy = min(y+d+1,src.shape[1])
            crop = src.read_band(1,window=((minx,maxx),(miny,maxy)))
            idx = np.argmax(crop)
            x2,y2 = np.unravel_index(idx, crop.shape)
            pt = to_longlat((minx+x2, miny+y2), src.affine)
    return pt

def from_longlat(pt, affine):
    y,x = ~affine*(pt)
    return x,y

def to_longlat(pt, affine):
    return affine*(pt[1],pt[0])
