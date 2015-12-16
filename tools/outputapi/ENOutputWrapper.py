'''

Wrapper for EPANET Output API.

Author: Bryant E. McDonnell
Date: 12/7/2015
Language: Anglais

'''

from ctypes import *
from _ENOutputToolkit import *
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




#int DLLEXPORT ENR_open(ENResultsAPI* enrapi, const char* path);
_OpenFunc = _library.ENR_open
_OpenFunc.argtypes = [c_void_p,c_char_p]

#int DLLEXPORT ENR_getNetSize(ENResultsAPI* enrapi, ENR_ElementCount code, int* count);
_GetNetSize = _library.ENR_getNetSize
_GetNetSize.argtypes = [c_void_p, c_int, POINTER(c_int)]

###int DLLEXPORT ENR_getUnits(ENResultsAPI* enrapi, ENR_Unit code, int* unitFlag);
_GetUnits = _library.ENR_getUnits
_GetUnits.argtypes = [c_void_p, c_int, POINTER(c_int)]

###int DLLEXPORT ENR_getTimes(ENResultsAPI* enrapi, ENR_Time code, int* time)
_getTimes = _library.ENR_getTimes
_getTimes.argtypes = [c_void_p, c_int, POINTER(c_int)]

###float* ENR_newOutValueSeries(ENResultsAPI* enrapi, int seriesStart,
###        int seriesLength, int* length, int* errcode);
_newOutValueSeries = _library.ENR_newOutValueSeries
_newOutValueSeries.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int)]
_newOutValueSeries.restype = POINTER(c_float)

###float* ENR_newOutValueArray(ENResultsAPI* enrapi, ENR_ApiFunction func,
###        ENR_ElementType type, int* length, int* errcode);
_newOutValueArray = _library.ENR_newOutValueArray
_newOutValueArray.argtypes = [c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_int)]
_newOutValueArray.restype = POINTER(c_float)

###int DLLEXPORT ENR_getNodeSeries(ENResultsAPI* enrapi, int nodeIndex, ENR_NodeAttribute attr,
###        int timeIndex, int length, float* outValueSeries, int* len);
_getNodeSeries = _library.ENR_getNodeSeries
_getNodeSeries.argtypes = [c_void_p, c_int, c_int, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getLinkSeries(ENResultsAPI* enrapi, int linkIndex, ENR_LinkAttribute attr,
###        int timeIndex, int length, float* outValueSeries);
_getLinkSeries = _library.ENR_getLinkSeries
_getLinkSeries.argtypes = [c_void_p, c_int, c_int, c_int, c_int, POINTER(c_float)]


###int DLLEXPORT ENR_getLinkID(ENResultsAPI* enrapi, int linkIndex, char* id);
_getLinkID = _library.ENR_getLinkID
_getLinkID.argtypes = [c_void_p, c_int, c_char_p]
###int DLLEXPORT ENR_getNodeID(ENResultsAPI* enrapi, int nodeIndex, char* id);
_getNodeID = _library.ENR_getNodeID
_getNodeID.argtypes = [c_void_p, c_int, c_char_p]


###int DLLEXPORT ENR_getNodeValue(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,
###       ENR_NodeAttribute attr, float *value);
_getNodeValue = _library.ENR_getNodeValue
_getNodeValue.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(c_float)]



###int DLLEXPORT ENR_getLinkValue(ENResultsAPI* enrapi, int timeIndex, int linkIndex, ENR_LinkAttribute attr, float *value)
_getLinkValue = _library.ENR_getLinkValue
_getLinkValue.argtypes = [c_void_p, c_int, c_int, c_int, POINTER(c_float)]


###int DLLEXPORT ENR_getNodeAttribute(ENResultsAPI* enrapi, int timeIndex,
###        ENR_NodeAttribute attr, float* outValueArray);
_getNodeAttribute = _library.ENR_getNodeAttribute
_getNodeAttribute.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENT_getLinkAttribute(ENResultsAPI* enrapi, int timeIndex,
###        ENR_LinkAttribute attr, float* outValueArray);
_getLinkAttribute = _library.ENR_getLinkAttribute
_getLinkAttribute.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getNodeResult(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,
###        float* outValueArray);
_getNodeResult = _library.ENR_getNodeResult
_getNodeResult.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_getLinkResult(ENResultsAPI* enrapi, int timeIndex, int linkIndex,
###        float* outValueArray);
_getLinkResult = _library.ENR_getLinkResult
_getLinkResult.argtypes = [c_void_p, c_int, c_int, POINTER(c_float)]

###int DLLEXPORT ENR_free(float *array);
_free = _library.ENR_free
_free.argtypes = [POINTER(c_float)]

###int DLLEXPORT ENR_close(ENResultsAPI* enrapi);
_CloseOut = _library.ENR_close
_CloseOut.argtypes = [c_void_p]

###int DLLEXPORT ENR_errMessage(int errcode, char* errmsg, int n);
_RetErrMessage = _library.ENR_errMessage
_RetErrMessage.argtypes = [c_int, c_char_p, c_int]


label = create_string_buffer(max_label_len)
errmsg = create_string_buffer(err_max_char)


class OutputObject(object):

    def OpenOutputFile(self, binfile):
        '''
        1) Initializes the opaque pointer to enrapi struct.
        2) Opens the output file.
        '''
        self.enrapi = c_void_p()
        ret = _OpenFunc(byref(self.enrapi), binfile)
        if ret != 0:
            self.RaiseError(ret)
        self._get_Units()
        self._get_NetSize()
        self._get_Times()

    def RaiseError(self, ErrNo):
        if _RetErrMessage(ErrNo , errmsg, err_max_char)==0:
            raise Exception(errmsg.value)
        else:
            raise Exception("Unknown error #{0}".format(ErrNo) )

    def _get_Units(self):
        '''
        Purpose: Returns pressure and flow units
        '''
        unit = c_int()
        _GetUnits(self.enrapi, ENR_flowUnits, unit)
        self.flowUnits = unit.value

        _GetUnits(self.enrapi, ENR_pressUnits, unit)
        self.pressUnits = unit.value
        
        
    def _get_NetSize(self):
        '''
        Populates object attributes with the water object counts
        '''
        count = c_int()
        _GetNetSize(self.enrapi, ENR_nodeCount, byref(count))
        self.nodeCount = count.value

        _GetNetSize(self.enrapi, ENR_tankCount, byref(count))
        self.tankCount = count.value

        _GetNetSize(self.enrapi, ENR_linkCount, byref(count))
        self.linkCount = count.value

        _GetNetSize(self.enrapi, ENR_pumpCount, byref(count))
        self.pumpCount = count.value

        _GetNetSize(self.enrapi, ENR_valveCount, byref(count))
        self.valveCount = count.value

    def _get_Times(self):
        '''
        Purpose: Returns report and simulation time related parameters.
        '''
        temp = c_int()
        _getTimes(self.enrapi, ENR_reportStart, byref(temp))
        self.reportStart = temp.value

        _getTimes(self.enrapi, ENR_reportStep, byref(temp))
        self.reportStep = temp.value
        
        _getTimes(self.enrapi, ENR_simDuration, byref(temp))
        self.simDuration = temp.value

        _getTimes(self.enrapi, ENR_numPeriods, byref(temp))
        self.numPeriods = temp.value


    def get_NodeID(self, index):
         """Retrieves the ID label of a node with a specified index.
       
         Arguments:
         index: node index"""
         _getNodeID(self.enrapi, index, label )
         return label.value

    def get_LinkID(self, index):
         """Retrieves the ID label of a link with a specified index.
       
         Arguments:
         index: link index"""
         _getLinkID(self.enrapi, index, label )
         return label.value


    def get_NodeValue(self, NodeInd, TimeInd,  NodeAttr):
        '''
        Purpose: Get results for particular node, time, attribute.
        '''
        xval= c_float()
        ierr= _getNodeValue(self.enrapi, TimeInd, NodeInd, NodeAttr, byref(xval) )
        if ierr == 0:
           return xval.value
        else:
           self.RaiseError(ierr)
           
    def get_LinkValue(self, NodeInd, TimeInd,  NodeAttr):
        '''
        Purpose: Get results for particular link, time, attribute.
        '''
        xval= c_float()
        ierr= _getLinkValue(self.enrapi, TimeInd, NodeInd, NodeAttr, byref(xval) )
        if ierr == 0:
           return xval.value
        else:
           self.RaiseError(ierr)




    def get_NodeSeries(self, NodeInd, NodeAttr, SeriesStartInd = 0, SeriesLen = -1):
        '''
        Purpose: Get time series results for particular attribute. Specify series
        start and length using seriesStart and seriesLength respectively.

        SeriesLen = -1 Default input: Gets data from Series Start Ind to end
        
        '''
        if SeriesLen > self.numPeriods :
            raise Exception("Outside Number of TimeSteps")
        elif SeriesLen == -1:
            SeriesLen = self.numPeriods
            
        sLength = c_int()
        ErrNo1 = c_int()            
        SeriesPtr = _newOutValueSeries(self.enrapi, SeriesStartInd,
                                            SeriesLen, byref(sLength), byref(ErrNo1))
        ErrNo2 = _getNodeSeries(self.enrapi, NodeInd, NodeAttr,
                                  SeriesStartInd, sLength.value, SeriesPtr)
        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        _free(SeriesPtr)
        return BldArray

    def get_LinkSeries(self, LinkInd, LinkAttr, SeriesStartInd = 0, SeriesLen = -1):
        '''
        Purpose: Get time series results for particular attribute. Specify series
        start and length using seriesStart and seriesLength respectively.

        SeriesLen = -1 Default input: Gets data from Series Start Ind to end
        
        '''
        if SeriesLen > self.numPeriods :
            raise Exception("Outside Number of TimeSteps")
        elif SeriesLen == -1:
            SeriesLen = self.numPeriods
            
        sLength = c_int()
        ErrNo1 = c_int()            
        SeriesPtr = _newOutValueSeries(self.enrapi, SeriesStartInd,
                                            SeriesLen, byref(sLength), byref(ErrNo1))
        ErrNo2 = _getLinkSeries(self.enrapi, LinkInd, LinkAttr,
                                  SeriesStartInd, sLength.value, SeriesPtr)
        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        ret = _free(SeriesPtr)

        return BldArray


    def get_NodeAttribute(self, NodeAttr, TimeInd):
        '''
        Purpose: For all nodes at given time, get a particular attribute
        '''
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _newOutValueArray(self.enrapi, ENR_getAttribute,
                                             ENR_node, byref(alength), byref(ErrNo1))
        ErrNo2 = _getNodeAttribute(self.enrapi, TimeInd, NodeAttr, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _free(ValArrayPtr)
        return BldArray

    def get_LinkAttribute(self, LinkAttr, TimeInd):
        '''
        Purpose: For all links at given time, get a particular attribute
        '''
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _newOutValueArray(self.enrapi, ENR_getAttribute,
                                             ENR_link, byref(alength), byref(ErrNo1))
        ErrNo2 = _getLinkAttribute(self.enrapi, TimeInd, LinkAttr, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _free(ValArrayPtr)
        return BldArray


    def get_NodeResult(self, NodeInd, TimeInd):
        '''
        Purpose: For a node at given time, get all attributes
        '''
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _newOutValueArray(self.enrapi, 
	                                ENR_getResult,
                                        ENR_node, 
					byref(alength), 
					byref(ErrNo1))
        ErrNo2 = _getNodeResult(self.enrapi, TimeInd, NodeInd, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _free(ValArrayPtr)
        return BldArray

    def get_LinkResult(self, LinkInd, TimeInd):
        '''
        Purpose: For a link at given time, get all attributes
        '''
        alength = c_int()
        ErrNo1 = c_int()
        ValArrayPtr = _newOutValueArray(self.enrapi, 
	                                ENR_getResult,
                                        ENR_link, 
					byref(alength), 
					byref(ErrNo1))
        ErrNo2 = _getLinkResult(self.enrapi, TimeInd, LinkInd, ValArrayPtr)
        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        _free(ValArrayPtr)
        return BldArray

    def CloseOutputFile(self):
        '''
        Call to close binary file.
        '''
        ret = _CloseOut(byref(self.enrapi) )
        if ret != 0:
            raise Exception('Failed to Close *.out file')
        




    
    
    
