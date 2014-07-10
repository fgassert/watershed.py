import numpy as np
cimport numpy as np

DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t

def watershed_from_d8(x, y, fd):
    if fd.dtype != np.uint8:
        fd = fd.astype(DTYPE)
    if type(x) is not int:
        x = int(x)
    if type(y) is not int:
        y = int(y)
    rows, cols = fd.shape
    return _watershed_from_d8(x,y,rows,cols,fd)

cdef object _watershed_from_d8(int x, int y, int rows, int cols, np.ndarray[DTYPE_t, ndim=2] fd):
    cdef np.ndarray inactive = np.zeros((rows,cols), dtype=DTYPE)
    # zero out raster borders as cheap error-catching hack
    fd[0,:]=0
    fd[rows-1,:]=0
    fd[:,0]=0
    fd[:,cols-1]=0
    
    return _flow_edge(x,y,fd,inactive)

cdef object _flow_edge(int x,int y,np.ndarray[DTYPE_t, ndim=2] fd, np.ndarray[DTYPE_t, ndim=2] inactive):
    inactive[x,y] = 1
    if fd[x  ,y-1] & 1   >0 and inactive[x  ,y-1]<1 : 
        _flow_edge(x  ,y-1,fd,inactive)

    if fd[x-1,y-1] & 2   >0 and inactive[x-1,y-1]<1 : 
        _flow_edge(x-1,y-1,fd,inactive)

    if fd[x-1,y  ] & 4   >0 and inactive[x-1,y  ]<1 : 
        _flow_edge(x-1,y  ,fd,inactive)

    if fd[x-1,y+1] & 8   >0 and inactive[x-1,y+1]<1 : 
        _flow_edge(x-1,y+1,fd,inactive)

    if fd[x  ,y+1] & 16  >0 and inactive[x  ,y+1]<1 : 
        _flow_edge(x  ,y+1,fd,inactive)

    if fd[x+1,y+1] & 32  >0 and inactive[x+1,y+1]<1 : 
        _flow_edge(x+1,y+1,fd,inactive)

    if fd[x+1,y  ] & 64  >0 and inactive[x+1,y  ]<1 : 
        _flow_edge(x+1,y  ,fd,inactive)

    if fd[x+1,y-1] & 128 >0 and inactive[x+1,y-1]<1 : 
        _flow_edge(x+1,y-1,fd,inactive)
    return inactive
