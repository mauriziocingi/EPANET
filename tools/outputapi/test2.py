import enoutwrap  as ENob

filename="net1.bin"  #"outapi.pyc" #
netout= ENob.open(filename)

print "nodes:",   ENob.getnetsize(netout, ENob.ENR_nodeCount )
print "tanks:",   ENob.getnetsize(netout, ENob.ENR_tankCount )
print "links:",   ENob.getnetsize(netout, ENob.ENR_linkCount )
print "pumps:",   ENob.getnetsize(netout, ENob.ENR_pumpCount )
print "valves:",  ENob.getnetsize(netout, ENob.ENR_valveCount )

numperiods= ENob.gettimes(netout, ENob.ENR_numPeriods)
index= 10
nodeID= ENob.getnodeid(netout, index)
print "\n\nHead at node index={0}, ID={1} for {2} periods".format( index, nodeID, numperiods)

for i in range(0, numperiods):
    print ENob.getnodevalue(netout, timeidx=i, nodeidx=index, attridx=ENob.ENR_head),
print "\n\n"

ENob.close(netout)