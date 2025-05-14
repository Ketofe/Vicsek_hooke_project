import numpy as np


def filter_out_blue_and_red_indexes(indexes,index_limit):
    blue_indexes=[]
    red_indexes=[]
    for index in indexes:
        if index<index_limit:
            blue_indexes.append(index)
        else:
              red_indexes.append(index)
    return np.array(blue_indexes),np.array(red_indexes)




#This will bee used to find the blue and red centers by taking the averag position in cluster it will be done for different itertions 
def find_center(pos,indexes):
         center=np.average(pos.transpose( (1,0,2) )[indexes],axis=0)   
         return center

                




#The following function takes away rotation from cluster . Also centers the cluster at 0 and makes it so that the blue center is in the xaxis
def take_away_rotation(pos,theta,cluster_indexes,blue_or_red_center,index_limit):
     number_of_iterations=len(pos)
     new_pos=np.zeros([number_of_iterations,len(cluster_indexes),2])
     new_theta=np.zeros([number_of_iterations,len(cluster_indexes)])
     #Creating theta and pos with only the indexes inside the cluster       #Undoing the data shaping once the indexes have been filtered out 
     pos_with_only_relevant_indexes=pos.transpose((1,0,2))[cluster_indexes].transpose((1,0,2))
     theta_with_only_relevant_indexes=theta.transpose()[cluster_indexes].transpose()
     #The indexes will changes this list will assign color to the new indexes
     colors = ['blue' if k < index_limit else 'red' for k in cluster_indexes]

     for i in range(number_of_iterations):
         cluster_center=np.average(pos_with_only_relevant_indexes[i],axis=0)
         shifted_blue_or_red_center=blue_or_red_center[i]-cluster_center
         rotation_angle=np.arctan2( shifted_blue_or_red_center[1],shifted_blue_or_red_center[0])
         #Now undoing the rotaion from theta
         new_theta[i]=theta_with_only_relevant_indexes[i]-rotation_angle
         #Inverse rotation matrix
         R_inverse=np.array([ [np.cos( rotation_angle),np.sin(rotation_angle)],[-np.sin(rotation_angle),np.cos( rotation_angle)] ])
         new_pos[i]= (  pos_with_only_relevant_indexes[i]-cluster_center)  @ R_inverse.T
     #Now rotating the whole cluster so that the blue center is a the x axis
     for i in range(number_of_iterations):
           blue_center = np.average(
    np.array([new_pos[i][k] for k in range(len(new_pos[i])) if colors[k] == 'blue']), 
    axis=0
)
           rotation_angle=np.arctan2( blue_center[1],blue_center[0])
           new_theta[i]=new_theta[i]-rotation_angle
           #Inverse roation matrix
           R_inverse=np.array([ [np.cos( rotation_angle),np.sin(rotation_angle)],[-np.sin(rotation_angle),np.cos( rotation_angle)] ])
           new_pos[i]=new_pos[i] @ R_inverse.T
     return new_pos,new_theta,colors
