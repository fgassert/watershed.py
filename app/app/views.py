from django.http import HttpResponse
from django.middleware.gzip import GZipMiddleware
import cached_watershed
import json
import os

CONTENT_TYPES = {'zip':'application/zip',
                 'json':'application/json',
                 'pjson':'text/json',
                 'tif':'application/octet-stream'}

gzip_middleware = GZipMiddleware()

def get_watershed(r):
    try:
        if r.method == 'GET':
            opts = r.GET
        elif r.method == 'POST':
            opts = r.POST
        if 'loc' in opts.keys():
            x,y = opts['loc'].split(',')
            pos = (float(x),float(y))
            snap = 0.00833333
            f = 'pjson'
            force = False
            if 'd' in opts.keys():
                snap = float(opts['d'])
            if 'f' in opts.keys():
                f = opts['f']
            if 'force' in opts.keys():
                force = True
            file_name = cached_watershed.get_watershed(pos,snap,f,force)
            if file_name is not None and f in CONTENT_TYPES.keys():
                with open(file_name,'rb') as src:
                    if f in ('json', 'pjson'):
                        t = src.read()
                        if f == 'pjson':
                            t = json.dumps(json.loads(t),indent=2)
                        res = HttpResponse(t, content_type=CONTENT_TYPES[f])
                        return gzip_middleware.process_response(r, res)
                    else:
                        res = HttpResponse(src.read(), content_type=CONTENT_TYPES[f])
                        res['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)
                        return res
        return HttpResponse("Invalid request", status=400)
    except:
        return HttpResponse("Invalid request: ERROR", status=400)
