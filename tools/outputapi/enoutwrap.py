import ctypes
import sys

if sys.platform=='linux2':
    libname= "./liboutputapi.so"
else:
    libname= "outputapi.dll"

try:
    _library = ctypes.CDLL(libname)
except:
    raise Exception('Failed to Open Linked Library')
    
_err_max_char= 80
_max_label_len= 32
errmsg = ctypes.create_string_buffer(_err_max_char)
label = ctypes.create_string_buffer(_max_label_len)

class EnOutErr(Exception):
  pass

def errcheck(ierr):
  if ierr==0: 
     return
  if _library.ENR_errMessage(ierr, ctypes.byref(errmsg), _err_max_char)==0:
     raise EnOutErr(errmsg.value)
  else:
     raise EnOutErr("Unknown error #{0}".format(ierr) )


#int DLLEXPORT ENR_open(ENResultsAPI* *penrapi, const char* path)
def open(filename):
    addr=ctypes.c_void_p()
    errcheck(_library.ENR_open(ctypes.byref(addr), filename)  )
    return addr

#int DLLEXPORT ENR_close(ENResultsAPI **enrapi);
def close(addr):
    errcheck(_library.ENR_close(ctypes.byref(addr)) )

#int DLLEXPORT ENR_getNetSize(ENResultsAPI* enrapi, ENR_ElementCount code, int* count);
def getnetsize(addr, elementcode):
    count= ctypes.c_int()
    errcheck(_library.ENR_getNetSize(addr, 
                                     elementcode, 
				     ctypes.byref(count)) )
    return count.value
    

def gettimes(addr, elementcode):
    count= ctypes.c_int()
    errcheck(_library.ENR_getTimes(addr,
                                   elementcode,
				   ctypes.byref(count)) )
    return count.value

# int DLLEXPORT ENR_getNodeValue(ENResultsAPI* enrapi, int timeIndex, int nodeIndex, ENR_NodeAttribute attr, float *value)
def getnodevalue(addr, timeidx, nodeidx, attridx):
    val= ctypes.c_float()
    errcheck(_library.ENR_getNodeValue(addr, timeidx, nodeidx, attridx, ctypes.byref(val)) )
    return val.value
    
#int DLLEXPORT ENR_getNodeID(ENResultsAPI* enrapi, int nodeIndex, char id[]);
def getnodeid(addr, index):
    """Retrieves the ID label of a node with a specified index.

    Arguments:
    index: node index"""    
    errcheck(_library.ENR_getNodeID(addr, index, ctypes.byref(label) ) )
    return label.value



ENR_nodeCount  = 1
ENR_tankCount  = 2
ENR_linkCount  = 3
ENR_pumpCount  = 4
ENR_valveCount = 5

ENR_demand   = 0
ENR_head     = 1
ENR_pressure = 2
ENR_quality  = 3

ENR_reportStart = 1
ENR_reportStep  = 2
ENR_simDuration = 3
ENR_numPeriods  = 4
