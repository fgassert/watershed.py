import watershed

loc = (40,-80)      # lat, lon
snap_distance = 1 # decimal degrees
outfile = 'my_watershed.geojson'

watershed.delineate_watershed(loc, outfile, snap_distance)

with open(outfile, 'r') as f:
    print(f.read())
