import numpy as np
#from scipy.spatial import cKDTree
from snnpy import build_snn_model







#In this model the particles will try make the distance between itself and other particles l. Or try to do the opposite.
#And alos aligng or anti align
                                                         #Here one can set initial conditions if not they wil be set to default values further down
def Vicsek_hooke(v_0,eta,r, N,L,iterations,s,k,l,initial_pos=None,initial_theta=None):
        theta=np.zeros([iterations,N])
        pos=np.zeros([iterations,N,2])
       
        if initial_pos is None:
               initial_pos= [ [np.random.uniform(0,L),np.random.uniform(0,L) ] for k in range(N) ]
        pos[0]=initial_pos
       
        if initial_theta is None:
               initial_theta=np.random.uniform(-np.pi,np.pi,N)
        theta[0]=initial_theta
        
     

        

        for iteration in range(iterations-1):
                
                #Here the neighbors are found
 
                #tree = cKDTree(pos[iteration],boxsize=[L,L])     #Added workers beneath for parallel processing
                #negibors=tree.query_ball_point(pos[iteration],r,workers=-1 ) 
                
                snn_model = build_snn_model(pos[iteration])
                negibors=[snn_model.query_radius(k, r) for k in pos[iteration]]


               #This is made using chat gpt
                # Filter out the particle's own index from its neighbors list 
                for particle_index in range(N):
                          negibors[particle_index] = [i for i in negibors[particle_index] if i != particle_index]
                
                #Now looping over all the particles and doing the angle update
                for particle_index in range(N):
                      self_angle=theta[iteration][particle_index]
                      self_pos=pos[iteration][particle_index]
                      negibor_indexes=negibors[particle_index]
                      number_of_neighbors=len(negibor_indexes)
                         
                      #Using if to deal with case when there are no neighbors 
                      if number_of_neighbors!=0:
                          
                          #First dealing with the part coming from the synchrnising orientations
                          orientation_interaction=s[particle_index][negibor_indexes]
                          #angle of neigbors               
                          neighbor_angles=theta[iteration][negibor_indexes]
                          complex_sum=np.exp(self_angle*1j)+sum(orientation_interaction*np.exp(neighbor_angles*1j))
                          angle_of_complex_sum=np.angle(complex_sum)

                          #Position of neighbors
                          neighbor_pos=pos[iteration][negibor_indexes]
                          interaction=k[particle_index][negibor_indexes]
                          

                          #This array stores the distance vectors between the particle and its neighbors   
                          distance_vectors=np.array([vec-self_pos for vec in neighbor_pos])
                          
                          abs_distance_vectors=np.array([np.linalg.norm(vec) for vec in distance_vectors ])
                          
                          #The displacement from the legnth l will be stored here
                          displacement=np.array([vec_size -l for vec_size in abs_distance_vectors])
                          
                          #Diving by this when normalising in order avoid divide by 0
                          divider=np.where(  abs_distance_vectors!=0,abs_distance_vectors,1)
                          #Here are normalised distnace vectors.
                          normalized_vectors=np.array([ distance_vectors[k]/divider[k] for k in range(number_of_neighbors) ])
                          forces=np.array([interaction[k]* normalized_vectors[k]*displacement[k] for k in range(number_of_neighbors) ])
                          F=np.sum(forces,axis=0)
                          

                          #Finally adding the forces and combing with the synchronizing result.
                          V=v_0*np.array([np.cos(angle_of_complex_sum),np.sin(angle_of_complex_sum)])+F
                          #Updating the angle and adding noise
                          theta[iteration+1][particle_index]=np.arctan2(V[1], V[0])+np.random.uniform(-eta,eta)
                           
                      else:
                          V=v_0*np.array([np.cos(self_angle),np.sin(self_angle)])
                          theta[iteration+1][particle_index]=self_angle+np.random.uniform(-eta,eta)
                      
                      #Updating positions               using % to deal with periodic boundary condition
                      pos[iteration+1][particle_index]=(self_pos+V)%L
                  
                             
                     
                     
        return pos,theta 

