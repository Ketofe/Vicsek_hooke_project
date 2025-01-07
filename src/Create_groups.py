import numpy as np
from find_group_index import * 








def Create_groups(group_relations,N,proporitons=None):
    s=np.zeros([N,N])
    k=np.zeros([N,N])
    
    #If not specified there will be the same amount of each group
    if proporitons==None:
        proporitons=np.ones(len(group_relations))/len(group_relations)
    
    #Each group will be between indexes. Now I am assigning the limit index of each group
    Index_limit_of_each_group=[] 
    limit_index=0
    for p in proporitons:
         limit_index=N*p+limit_index
         Index_limit_of_each_group.append(limit_index)
    Index_limit_of_each_group=np.array(Index_limit_of_each_group)


    for particle_index1 in range(N):
        #Now find the group index of the particle
        #Dealing with boundaris
        group_index1=find_group_index(Index_limit_of_each_group,particle_index1)


        for particle_index2 in range(N):
                        group_index2=find_group_index(Index_limit_of_each_group,particle_index2)

                        #Finnally assining the s an k
                        s[particle_index1][particle_index2]=group_relations[group_index1][group_index2][0]
                        k[particle_index1][particle_index2]=group_relations[group_index1][group_index2][1]

    return s,k