functions=[]
with open("../toolkit.tex", 'r') as fi:
  for line in fi:
    w= line.strip()
    if w.startswith("\input{"):
        functions.append( w.partition("{")[2].partition("}")[0].split("/")[-1] )
    else:
        #print w
        pass

included=[]
with open("lista.txt", 'r') as fi:
  for line in fi:
    j= line.index(".")  
    w= line[:j]
    if w not in functions:
        included.append(w)
    else:
        functions.remove(w)
        
print ', '.join(included)        

if len(functions)!=0:        
  print "\n\nundocumented function references",
  print functions
