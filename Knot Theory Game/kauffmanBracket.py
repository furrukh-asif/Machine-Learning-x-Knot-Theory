from math import factorial
import copy

def KauffmanState(pd,statevec):
    resolved_pd=[]
    for x in range(len(statevec)):
        if statevec[x]==0:
            resolved_pd.append([pd[x][0],pd[x][1]])
            resolved_pd.append([pd[x][2],pd[x][3]])
        if statevec[x]==1:
            resolved_pd.append([pd[x][3],pd[x][0]])
            resolved_pd.append([pd[x][1],pd[x][2]])
    edge_list=[*range(1,2*len(statevec)+1,1)]
    components=[]
    while len(edge_list)>0:
        components.append([edge_list[0]])
        edge_list.pop(0)
        i=0
        while i<len(components[-1]):
            neighbors=[]
            for x in range(len(resolved_pd)):
                if resolved_pd[x][0]==components[-1][i] and resolved_pd[x][1] in edge_list:
                    neighbors.append(resolved_pd[x][1])
                if resolved_pd[x][1]==components[-1][i] and resolved_pd[x][0] in edge_list:
                    neighbors.append(resolved_pd[x][0])
            neighbors=list(set(neighbors))
            for x in range(len(neighbors)):
                components[-1].append(neighbors[x])
                edge_list.remove(neighbors[x])
            i+=1
    return components
    
def StateVector(vec_num,digits):
    st_vec=list(bin(vec_num))
    st_vec.pop(0)
    st_vec.pop(0)
    for x in range(len(st_vec)):
        st_vec[x]=int(st_vec[x])
    for _ in range(digits-len(st_vec)):
        st_vec.insert(0,0)
    return st_vec

  
def binomial(x, y):
    try:
        return factorial(x) // factorial(y) // factorial(x - y)
    except ValueError:
        return 0
        
def KauffmanContribution(kstate,statevec,crossings):
    kvec=[3*crossings,[]]
    for _ in range(6*crossings+1):
        kvec[1].append(0)
    aexp=0
    for x in range(len(statevec)):
        if statevec[x]==0:
            aexp=aexp+1
        if statevec[x]==1:
            aexp=aexp-1
    topdegree=2*len(kstate)-2+aexp
    index=-3*crossings+topdegree-1
    sign=(-1)**(len(kstate)-1)
    for x in range(len(kstate)):
        kvec[1][index]=sign*binomial(len(kstate)-1,x)
        index=index-4
    return kvec
    
def listadd(list1,list2):
    sumlist=list1
    for x in range(len(list1)):
        sumlist[x]=sumlist[x]+list2[x]
    return sumlist

def trim(kvec):
    if kvec[1][0]==0:
        kvec[1].pop(0)
        return trim(kvec)
    if kvec[1][-1]==0:
        kvec[0]=kvec[0]-1
        kvec[1].pop(-1)
        return trim(kvec)
    return kvec
    
def KauffmanBracket(pd):
    crossings=len(pd)
    kb=KauffmanContribution(KauffmanState(pd,StateVector(0,crossings)),StateVector(0,crossings),crossings)
    for x in range(1,2**crossings,1):
        kvec=KauffmanContribution(KauffmanState(pd,StateVector(x,crossings)),StateVector(x,crossings),crossings)
        kb[1]=listadd(kb[1],kvec[1])
    kb=trim(kb)
    return kb
