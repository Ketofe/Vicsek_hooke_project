import matplotlib.pyplot as plt
from find_group_index import *
import numpy as np





def Quiver(pos,theta,colors,proportions=None):
    fig, ax = plt.subplots(figsize=(6, 6))
     #The number of particles
    N=len(pos)
    if proportions==None:
         proportions=np.ones(len(colors))/len(colors)
    limit_index=0
    Index_limit_of_each_group=[]
    for p in proportions:
         limit_index=N*p+limit_index
         Index_limit_of_each_group.append(limit_index)
    Index_limit_of_each_group=np.array(Index_limit_of_each_group)



    # Set up the initial quiver plot
    qv = ax.quiver(pos[:, 0], pos[:, 1], np.cos(theta), np.sin(theta))
    c = np.array([ colors[find_group_index(Index_limit_of_each_group,idx)] for idx in range(N)])
    qv.set_color(c)