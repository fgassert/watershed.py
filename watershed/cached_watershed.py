import watershed
import os
import sys

CACHE = "cache"
EXTS = {'shp':'.shp','pjson':'.json','json':'.json','tif':'.tif','zip':'.zip'}

def get_watershed(pt, d=0, f='zip',force=False):
    if d>0:
        pt = watershed.snap_to_highest(pt, d)
    
    if f in EXTS.keys():
        ext = EXTS[f]

    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)

    o = os.path.join(CACHE,_hashed(pt)+ext)
    if not os.path.isfile(o) or force:
        watershed.delineate_watershed(pt, o)
    return o

def _hashed(pt):
    return hex(abs(hash(pt)))[1:]

if __name__ == "__main__":
    if len(sys.argv)>2:
        pt = (float(sys.argv[1]), float(sys.argv[2]))
        if len(sys.argv)==3:
            print get_watershed(pt)
        if len(sys.argv)==4:
            print get_watershed(pt, float(sys.argv[3]))
        if len(sys.argv)==5:
            print get_watershed(pt, float(sys.argv[3]), sys.argv[4])
