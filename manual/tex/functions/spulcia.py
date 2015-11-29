def maketex(name, declaration, args):
    f= open(name+".tex","w")
    f.write("\\subsection{{{0}}}\n".format(name))
    f.write("\\subsubsection{Declaration}\n")
    f.write("\\begin{lstlisting}\n")
    f.write(declaration+"\n")
    f.write("\\end{lstlisting}\n")
    f.write("\\subsubsection{Description}\n** insert description here **\n")
    if len(args) > 0:
      f.write("\\subsubsection{Arguments}\n")
      f.write("\\begin{tabular}{l r p{11cm} }\n")
      for i in args:
        f.write("{0[0]}&{0[1]}&*insert arg description here* \\\\[6pt]\n".format(i))
      f.write("\\end{tabular}\n")
    f.write("\\subsubsection{Returns}\n")
    f.write("Returns an error code.\n")
    f.write("\\subsubsection{Notes}\n")
    f.write("* insert notes here *")   
 

    f.close()   


with open("../../../include/epanet2.h", 'r') as fi:
  for line in fi:
    w= line.split()
    if len(w)>2 and w[0]=="int" and w[1]=="DLLEXPORT":
        declaration = ' '.join(w[2:])
        j= declaration.index("(")
        name = declaration[:j]
        declaration= w[0]+' '+declaration
        declaration = declaration.replace("EN_API_FLOAT_TYPE", "float") 
        j= declaration.index("(")       
        linearg= declaration[j+1:].rstrip(");")
        print "\n",name
        print declaration
        args=[]
        if linearg!="":
          for i in linearg.split(","):
            aa= i.split()
            tipo= aa[0]
            nome= aa[1]
            if nome[0]=="*":
                nome= nome[1:]
                tipo+= " pointer"
            args.append((tipo, nome))
        maketex(name,declaration,args)




     