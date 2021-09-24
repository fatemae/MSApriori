# -*- coding: utf-8 -*-
# MSAPriori Algorithm
# Fatema Engineeringwala
# Pallavi Krishna Bhat

import itertools

n = 0
transaction = []
MIS = {}
support_count = {}
rest = []

#readData: Read and store data in input files into variables
def readData():
    transaction=[]
    MIS={}
    with open('HW1-data.txt', 'r') as transactions:
        for data in transactions:
            transaction.append([x.strip() for x in data.split(',')])
    # print(transaction)
    n=len(transaction)
    with open('HW1-parameter.txt', 'r') as params:
        for data in params:
            valType=data.split('=')[0].strip()
            value=data.split('=')[1].strip()
            if(valType=='SDC'):
                sdc=float(value)
            else :
                valType=valType[valType.find('(')+1:valType.find(')')]
                MIS[valType]=float(value)	
    # print(MIS)
    for t in transaction:
        for item in t:
            if(item not in MIS.keys() and item not in rest):
                rest.append(item)
    return transaction,MIS,n,sdc
#Sort items as per their MIS values
def sort(MIS):
    M={}
    for item,mis in sorted(MIS.items(), key=lambda x: x[1]):
        if item=="rest":
            for i in rest:
                M[i]=mis
        else : M[item]=mis
    return M
#Init Pass to generate L and support count
def init_pass(M,transaction):
    items = []
    for l in transaction :
        for str in l:
            if str not in items:
                items.append(str)
            if str not in support_count:
                support_count[str] = l.count(str)
            else :
                support_count[str]+=l.count(str)
    print("support_count:",end='')
    print(support_count)
    L=[]
    i=None
    for item in M:
        if i is not None:
            if(item in support_count.keys() and support_count[item]/n >= M[i]):
                L.append(item)
        else:
            if(item in support_count.keys() and support_count[item]/n >= M[item]):
                L.append(item)
                i=item

    print("L:",end='')
    print(L)
    return support_count,L
#Generate Candidate keys for k=2
def level2_candidate_gen(L, sdc):
    C2 = []
    for i,l in enumerate(L):
        k=l
        if(l not in MIS.keys()):
            k='rest'
        if(support_count[l]/n >= MIS[k]):
            for h in range(i+1,len(L)):
                if(support_count[L[h]]/n >= MIS[k] and abs(support_count[L[h]]-support_count[l])/n <= sdc):
                    C2.append([l,L[h]])
    return C2
#Candidate generation for k>2
def MScandidate_gen(F,sdc):
    Ck = []
    for f1 in F:
        for f2 in F:
            if(f1!=f2 and f1[:-1]==f2[:-1] and f1[-1]<f2[-1] and abs(support_count[f1[-1]]-support_count[f2[-1]])/n <= sdc):
                c=f1+f2[-1:]
                Ck.append(c)
                s_list=list(itertools.combinations(c,len(c)-1))
                for s in s_list:
                    key1,key2=c[0],c[1]
                    if(c[0] in rest):
                        key1='rest'
                    if(c[1] in rest):
                        key2='rest'
                    if(c[0] in s or MIS[key2]==MIS[key1]):
                        if list(s) not in F:
                            Ck.remove(c)
                            break
    return Ck
#Main: Includes the logic to find the final set of keys
def main():
    global n,MIS,transaction,support_count
    transaction=[]
    MIS={}
    transaction,MIS,n,sdc=readData()
    M = sort(MIS)
    support_count,L = init_pass(M,transaction)
    print("M:",end='')
    print(M)
    F = [[]]
    C = {}
    F.append([])
    for l in L:
        if (l not in MIS.keys()):
            if(support_count[l]/n >= MIS['rest']):
                F[1].append(l)  
        elif (support_count[l]/n >= MIS[l]):
            F[1].append(l)
    k=2
    while len(F[k-1])!=0:
        F.append([])
        if k==2 :
            C[k] = level2_candidate_gen(L, sdc)
        else : 
            C[k] = MScandidate_gen(F[k-1],sdc)
        candidate_count={}
        for t in transaction:
            for c in C[k]:
                if(set(c).issubset(set(t))):
                    if tuple(c) not in candidate_count.keys():
                        candidate_count[tuple(c)]=1
                    else: candidate_count[tuple(c)]+=1
        for c in candidate_count.keys():
            support_count[c]=candidate_count[c]
        for c in C[k]:
            temp=c[0]
            if(c[0] not in MIS.keys()):
                temp='rest'

            #if (support_count[tuple(c)]/ n >= MIS[temp]):
            if(support_count.get(tuple(c),0)/n >= MIS[temp]): #Pallavi1
                F[k].append(c)
        k+=1
        print('F:'+str(F))
    print(support_count)
    #Print to the output file
    outline=''
    for i,f in enumerate(F):
        if(i!=0):
            if len(f)>0 :
                outline += ("(Length-"+str(i)+" "+str(len(f)))
                for item in f:
                    outline+= "\n"
                    outline+= "\t("
                    outline+= (str(' '.join(item)) +")" if isinstance(item, list)  else item +")")
                outline+= (")\n")
    print(outline)
    outfile = open("output.txt", "w")
    outfile.write(outline)

if __name__=="__main__":main()