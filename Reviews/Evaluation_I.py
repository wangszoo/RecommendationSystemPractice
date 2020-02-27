import math 
import numpy as np 

//Root mean square error
def RMSE(records):
    return math.sqrt(\
    sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records])\
    / float(len(records)))

//Mean absolute error
def MAE(records):
    return sum([abs(rui-pui) for u,i,rui,pui in records])\
    / float(len(records))

    