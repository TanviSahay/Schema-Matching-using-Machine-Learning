from numpy import genfromtxt, savetxt
import numpy as np

#pollution data
Data = genfromtxt(open('./HP.csv','r'),dtype=float, delimiter=',')[1:]
Labels = Data[:,0]
print Labels

Data = Data[:,1:]
header= genfromtxt(open('./HP.csv','r'),delimiter=',',dtype = None)[0]
header = header[1:]

