import outapi
import ctypes
_err_max_char= 80

errmsg = ctypes.create_string_buffer(_err_max_char)

def err_check(ierr):
  if ierr==0: 
     return
  if outapi.RetErrMessage(ierr, ctypes.byref(errmsg), _err_max_char)==0:
     raise Exception(errmsg.value)
  else:
     raise Exception("Unknown error #{0}".format(ierr) )
     

addr=ctypes.c_void_p()
filename= "Net1.bin"
err_check(outapi.OpenFunc(ctypes.byref(addr), filename) )
print "\nfile {0} successfuly opened\n".format(filename)
k=ctypes.c_int()

err_check(outapi.GetNetSize(addr, outapi.ENR_nodeCount, k) )
print "nodes:     {0}".format(k.value)

err_check(outapi.GetNetSize(addr, outapi.ENR_tankCount, k) )
print "tanks:     {0}".format(k.value)

err_check(outapi.GetNetSize(addr, outapi.ENR_linkCount, k) )
print "links:     {0}".format(k.value)

err_check(outapi.GetNetSize(addr, outapi.ENR_pumpCount, k) )
print "pumps:     {0}".format(k.value)

err_check(outapi.GetNetSize(addr, outapi.ENR_valveCount, k) )
print "valves:     {0}".format(k.value)



err_check(outapi.getTimes(addr, outapi.ENR_numPeriods, k) )
numperiods= k.value
x= ctypes.c_float()
print "\n\nHead at node 10  "
for i in range(0, numperiods):
    err_check( outapi.getNodeValue(addr, i, 10, outapi.ENR_head, ctypes.byref(x)))
    print x.value,
print "\n\n"


err_check(outapi.CloseOut(ctypes.byref(addr)) )
print "\nfile {0} successfuly closed".format(filename)

#err_check(outapi.GetNetSize(addr, 1, k))


