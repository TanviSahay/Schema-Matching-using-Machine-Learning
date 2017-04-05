import numpy as np
from scipy import stats
import scipy
import re
#Character Feature Extraction
feature_dict={}
feature_vector=[]
#Extract TYPE UNIQUE NULL and KEY from Database

def Numberofbackslash(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    count_space=0
    i=len(charAttribute)
    for val in range(0,i):
        if(charAttribute[val]=="/"):
            count_space=count_space+1
    ratio=count_space*1.0/i
    return round(ratio,4)

def Numberofbrackets(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    count_space=0
    i=len(charAttribute)
    for val in range(0,i):
        if(charAttribute[val]=="("):
            count_space=count_space+1
    ratio=count_space*1.0/i
    return round(ratio,4)

def Numberofhyphen(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    count_space=0
    i=len(charAttribute)
    for val in range(0,i):
        if(charAttribute[val]=="-"):
            count_space=count_space+1
    ratio=count_space*1.0/i
    return round(ratio,4)

def NumbertoAll(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    count_integer=0
    i=len(charAttribute)
    for val in range(0,i):
        try:
            va=int(charAttribute[val])
            count_integer=count_integer+1
        except ValueError:
            continue
        val=val+1
    ratio=count_integer*1.0/i
    return round(ratio,4)

def ChartoAll(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    count_char=0
    i=len(charAttribute)
    for val in range(0,i):
        try:
            va=int(charAttribute[val])
        except ValueError:
            count_char=count_char+1
        val=val+1
    ratio=count_char*1.0/i
    return round(ratio,4)
    
def WhiteSpaceFeature(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    count_space=0
    i=len(charAttribute)
    for val in range(0,i):
        if(charAttribute[val]==" "):
            count_space=count_space+1
    ratio=count_space*1.0/i
    return round(ratio,4)
            
fixed_length=100
def averageusedlength(charAtt,n,fixed_length):
    charAttribute="".join(str(elm) for elm in charAtt)
    used_length=len(charAttribute)
    ratio=used_length*1.0/n*fixed_length
    return round(ratio,4)

#define used length array
passList=[]
lengtharray=[]
for values in passList:
    lengtharray.append(len(values))
    
def varianceoflength(passList,fixed_length): 
    lengtharray=[]
    for values in passList:
        lengtharray.append(len(str(values))) 
    return round(np.var(lengtharray)/fixed_length,4)
        
def varianceCoefflength(passList):
    lengtharray=[]
    for values in passList:
        lengtharray.append(len(str(values))) 
    return round(scipy.stats.variation(lengtharray, axis=0),4)
    
def isNull(passList):
    for values in passList:
        if(values is None):
            return 1           

def chartoLength(charAttribute):
    i=len(charAttribute)
    count_char=0
    for char in charAttribute:
        if(char.isalpha()):
            count_char=count_char+1
    ratio=count_char*1.0/i
    return round(ratio,4)

def specialChars(charAtt):
    charAttribute="".join(str(elm) for elm in charAtt)
    i=len(charAttribute)
    count_special=0
    for char in charAttribute:
        if (re.match("^[a-zA-Z0-9_/-(]*$", char)):
            continue 
        else:
           count_special=count_special+1          
    ratio=count_special*1.0/i
    return round(ratio,4)

#Numeric Feature Extraction
fixed_length=100
def numFeatures(numArray,fixed_length,n):
    sum=0
    n=len(numArray)
    for i in range(0,len(numArray)):
        if numArray[i] is None:
            numArray[i]=0         
    for values in numArray:
        sum=sum+values
    print sum,"zhjhdfgdfjhgdhg"
    avg=sum/n
    var=np.var(numArray)/(n)
    coeff=scipy.stats.variation(numArray, axis=0)
    mini=min(numArray)
    maxi=max(numArray)
    return float(avg),float(var),round(coeff,4),round(mini,4),round(maxi,4)
    

    
        

