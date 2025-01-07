import numpy as np
import pandas as pd
from trackpy.static import pair_correlation_2d
from find_group_index import *

#Returns array with position sorted after groups
def filter_out_group_pos(pos,proporitons):
    N=len(pos)
    pos_groups=[[] for k in proporitons]
    #Each group will be between indexes. Now I am assigning the limit index of each group
    Index_limit_of_each_group=[] 
    limit_index=0
    for p in proporitons:
         limit_index=N*p+limit_index
         Index_limit_of_each_group.append(limit_index)
    Index_limit_of_each_group=np.array(Index_limit_of_each_group)
    for n,p in enumerate(pos):
        group_index=find_group_index(Index_limit_of_each_group,n)
        pos_groups[group_index].append(p)
    
    #Converting the inner part to array
    return [ np.array(k) for k in pos_groups]


#Function that only includes position particles that are in the box 
def return_partilces_from_box_pos(pos,x_l,x_u,y_l,y_u):
    filtered_pos=[]
    for p in pos:
        if x_l<p[0]<x_u and y_l<p[1]<y_u:
            filtered_pos.append(p)
    return np.array(filtered_pos)


#Function that returns indexes within a cluster  
def return_partilces_from_box_indexes(pos,x_l,x_u,y_l,y_u):
    filtered_index=[]
    for n,p in enumerate(pos):
        if x_l<p[0]<x_u and y_l<p[1]<y_u:
            filtered_index.append(n)
    return np.array(filtered_index)



#This computes tha pair correlation function
def rdf(pos,dr,cuttof):
    #Coverting pandas data frame
    coverted_pos=pd.DataFrame(pos, columns=['x', 'y'])
    g=pair_correlation_2d(coverted_pos,cuttof,dr=dr)
    g_r=g[1]
    r_edges=g[0]
    r_centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    return r_centers, g_r