# -*- coding: utf-8 -*-
# MSAPriori Algorithm
# Fatema Engineeringwala  

import pandas as pd
import math
import copy
import csv
import re    

def MSApriori(examples, attribute, parent_examples,depth):
    if(examples.empty):
        return PluralityValue(parent_examples)
    elif(sameClassification(examples)):
        return examples['Result'][0]
    elif(not attribute):
        return PluralityValue(examples)
    else:
        # A = max((Importance(a,examples),a) for a in attribute)[1]
        I={}
        for a in attribute:
            I[a]=(Importance(a,examples))
        max_value = max(I.values())
        max_keys = [k for k, v in I.items() if v == max_value]
        A=max_keys[0]
        tree = Node(depth)
        tree.childs=[]
        tree.value=A
        attr=attribute
        attr.remove(A)
        for v in allExamples[A].unique():
            exs=examples[examples[A] == v]
            exs=exs.reset_index(drop=True)
            subtree = DecisionTreeLearning(exs,attr,examples,depth+1)
            if(isinstance(subtree,Node)):
                subtree.branch = v
                tree.childs.append(subtree)
            else:
                child=Node(depth+1)
                child.value=subtree
                child.branch=v
                tree.childs.append(child)
        return tree

def readData():
    transaction=[]
    MIS={}
    with open('HW1-data.txt', 'r') as transactions:
        for data in transactions:
            transaction.append([x.strip() for x in data.split(',')])
    print(transaction)
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
    print(MIS)
    return transaction,MIS,n

def sort(MIS):
    M=[]
    for item,mis in sorted(MIS.items(), key=lambda x: x[1]):
        M.append(item)
    return M

def init_pass(M,transaction):
    support_count={}	
    for l in transaction :
        for str in l:
            if str not in support_count:
                support_count[str] = l.count(str)
            else :
                support_count[str]+=l.count(str)
    print(support_count)
    return support_count

def printTree(start, tree, indent_width=4):

    def ptree(start, tree, indent="   "):
        if tree.depth == start:
            if tree.childs is None:
                if(tree.branch is None):
                    print(tree.value)
                else:
                    print("("+tree.branch+")--"+tree.value)
            else:
                if(tree.branch is None):
                    print(tree.value)
                else:
                    print("("+tree.branch+")--"+tree.value)
                for child in tree.childs[:-1]:
                    # print(indent + "├" + "─" * indent_width, end="")
                    print(indent + "├" + "─" * indent_width, end="")
                    ptree(tree.depth+1, child, indent + "│" + " " * 14)
        # if parent not in tree:
                child = tree.childs[-1]
                print(indent + "└" + "─" * indent_width, end="")
                ptree(tree.depth+1, child, indent + " " * 15)  # 4 -> 5

    parent = start
    ptree(start, tree)


def main():
    # global allExamples
    transaction=[]
    MIS={}
    n=0 
    transaction,MIS,n=readData()
    M=sort(MIS)
    print(M,T)

    
    # allExamples=a
    # colnames.remove('Result')
    # x=DecisionTreeLearning(a,colnames,a,0)
    # print("############### Decision Tree ############")
    # printTree(0,x)

    # print("\n\n############### Pruned Decision Tree ############")
    # statisticalSignificanceTest(x,a)
    # # x=sameClassification(a)
    # printTree(0,x)

if __name__=="__main__":main()