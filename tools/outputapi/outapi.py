from ctypes import *

import platform

_plat= platform.system()
if _plat=='Linux':
  _libname = "./liboutputapi.so"
elif _plat=='Windows':
  _libname = "outputapi.dll"
else:
  Exception('Platform '+ _plat +' unsupported (not yet)')


try:
    _library = CDLL(_libname)
except:
    raise Exception('Failed to {0}'.format(_libname) )
    

###int DLLEXPORT ENR_open(ENResultsAPI* enrapi, const char* path);
OpenFunc = _library.ENR_open
OpenFunc.argtypes = [c_void_p,c_char_p]

###int DLLEXPORT ENR_getNetSize(ENResultsAPI* enrapi, ENR_ElementCount code, int* count);
GetNetSize = _library.ENR_getNetSize
GetNetSize.argtypes = [c_void_p, c_int, POINTER(c_int)]

###int DLLEXPORT ENR_getUnits(ENResultsAPI* enrapi, ENR_Unit code, int* unitFlag);
GetUnits = _library.ENR_getUnits
GetUnits.argtypes = [c_void_p, c_int, POINTER(c_int)]

###int DLLEXPORT ENR_getTimes(ENResultsAPI* enrapi, ENR_Time code, int* time)
getTimes = _library.ENR_getTimes
getTimes.argtypes = [c_void_p, c_int, POINTER(c_int)]

###int DLLEXPORT ENR_getNodeValue(ENResultsAPI* enrapi, int timeIndex, int nodeIndex, ENR_NodeAttribute attr, float *value);
getNodeValue =   _library.ENR_getNodeValue
getNodeValue.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(c_float)]

###float* ENR_newOutValueSeries(ENResultsAPI* enrapi, int seriesStart,
###        int seriesLength, int* length, int* errcode);
newOutValueSeries = _library.ENR_newOutValueSeries
newOutValueSeries.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int)]
newOutValueSeries.restype = POINTER(c_float)

###float* ENR_newOutValueArray(ENResultsAPI* enrapi, ENR_ApiFunction func,
###        ENR_ElementType type, int* length, int* errcode);
newOutValueArray = _library.ENR_newOutValueArray
newOutValueArray.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int)]
newOutValueArray.restype = POINTER(c_float)

###int DLLEXPORT ENR_getNodeSeries(ENResultsAPI* enrapi, int nodeIndex, ENR_NodeAttribute attr,
###        int timeIndex, int length, float* outValueSeries, int* len);
getNodeSeries = _library.ENR_getNodeSeries
getNodeSeries.argtypes = [c_void_p, c_int, c_int, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getLinkSeries(ENResultsAPI* enrapi, int linkIndex, ENR_LinkAttribute attr,
###        int timeIndex, int length, float* outValueSeries);
getLinkSeries = _library.ENR_getLinkSeries
getLinkSeries.argtypes = [c_void_p, c_int, c_int, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getNodeAttribute(ENResultsAPI* enrapi, int timeIndex,
###        ENR_NodeAttribute attr, float* outValueArray);
getNodeAttribute = _library.ENR_getNodeAttribute
getNodeAttribute.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENT_getLinkAttribute(ENResultsAPI* enrapi, int timeIndex,
###        ENR_LinkAttribute attr, float* outValueArray);
getLinkAttribute = _library.ENR_getLinkAttribute
getLinkAttribute.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getNodeResult(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,
###        float* outValueArray);
getNodeResult = _library.ENR_getNodeResult
getNodeResult.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getLinkResult(ENResultsAPI* enrapi, int timeIndex, int linkIndex,
###        float* outValueArray);
getLinkResult = _library.ENR_getLinkResult
getLinkResult.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_free(float *array);
free = _library.ENR_free
free.argtypes = [POINTER(c_float)]

###int DLLEXPORT ENR_close(ENResultsAPI* enrapi);
CloseOut = _library.ENR_close
CloseOut.argtypes = [c_void_p]

###int DLLEXPORT ENR_errMessage(int errcode, char* errmsg, int n);
RetErrMessage = _library.ENR_errMessage
RetErrMessage.argtypes = [c_int, c_void_p, c_int]

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



