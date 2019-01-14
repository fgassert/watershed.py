import numpy as np
cimport numpy as np

DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t

def watershed_from_d8(y, x, fd):
    ''''''
    if fd.dtype != np.uint8:
        fd = fd.astype(DTYPE)
    if type(x) is not int:
        x = int(x)
    if type(y) is not int:
        y = int(y)
    rows, cols = fd.shape
    return _watershed_from_d8(y, x, rows, cols, fd)

cdef np.ndarray[DTYPE_t, ndim=2] _watershed_from_d8(int y, int x, int rows, int cols, np.ndarray[DTYPE_t, ndim=2] fd):
    cdef np.ndarray inactive = np.zeros((rows,cols), dtype=DTYPE)
    # zero out raster borders as cheap error-catching hack
    fd[0, :]=0
    fd[rows-1, :]=0
    fd[:, 0]=0
    fd[:, cols-1]=0
    
    return _flow_edge(y, x, fd, inactive)

cdef np.ndarray[DTYPE_t, ndim=2] _flow_edge(int y, int x, np.ndarray[DTYPE_t, ndim=2] fd, np.ndarray[DTYPE_t, ndim=2] inactive):
    inactive[y, x] = 1
    if fd[y  ,x-1] & 1   >0 and inactive[y  ,x-1]<1 : 
        _flow_edge(y  ,x-1,fd,inactive)

    if fd[y-1,x-1] & 2   >0 and inactive[y-1,x-1]<1 : 
        _flow_edge(y-1,x-1,fd,inactive)

    if fd[y-1,x  ] & 4   >0 and inactive[y-1,x  ]<1 : 
        _flow_edge(y-1,x  ,fd,inactive)

    if fd[y-1,x+1] & 8   >0 and inactive[y-1,x+1]<1 : 
        _flow_edge(y-1,x+1,fd,inactive)

    if fd[y  ,x+1] & 16  >0 and inactive[y  ,x+1]<1 : 
        _flow_edge(y  ,x+1,fd,inactive)

    if fd[y+1,x+1] & 32  >0 and inactive[y+1,x+1]<1 : 
        _flow_edge(y+1,x+1,fd,inactive)

    if fd[y+1,x  ] & 64  >0 and inactive[y+1,x  ]<1 : 
        _flow_edge(y+1,x  ,fd,inactive)

    if fd[y+1,x-1] & 128 >0 and inactive[y+1,x-1]<1 : 
        _flow_edge(y+1,x-1,fd,inactive)
    return inactive
