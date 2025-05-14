
import numpy as np
from scipy.cluster.vq import whiten, kmeans, vq, kmeans2


def get_clusters(pos, number_of_clusters):
    centers, _ = kmeans(pos, number_of_clusters)  # Perform k-means clustering
    cluster_labels, _ = vq(pos, centers)         # Assign cluster labels to each point

    # Create a list of empty lists to hold indices for each cluster
    clusters = [[] for _ in range(number_of_clusters)]
    for idx, label in enumerate(cluster_labels):
        clusters[label].append(idx)  # Append the index to the correct cluster
    
    return clusters


#Every index below the index limit is blue above is red.
def filter_out_blue_and_red_from_cluster(clusters, index_limit):
        blue_clusters=[]
        red_clusters=[]
        for cluster in clusters:
            blue_clusters.append([idx for idx in cluster if idx <index_limit])
            red_clusters.append([idx for idx in cluster if idx >=index_limit])
        return blue_clusters, red_clusters



#This will bee used to find the blue and red centers by taking the averag position in cluster it will be done for different itertions 
def find_centers(pos,clusters):
         cluster_centers=[]
         for cluster in clusters:
                                 #Here average of cluster gets taken for multiple iterations. The transpose is to reshape the data
                                center=np.average(pos.transpose( (1,0,2) )[cluster],axis=0)               
                                cluster_centers.append(center)
                                       
         return cluster_centers


#This function returns positions or orientaions in list of arrays where each array corresponds to a cluster
def sort_property_into_clusters(property,clusters):
    sorted_property=[]
    for cluster in clusters:
        sorted_property.append(property[cluster] )
    return sorted_property




#Functions that will be used for frequncy anlalysis pos_list contains the position of different particles. It should be like this [pos_particle0,pos_particle1...
#Chat gpt helped with this
def F(pos_list, cut_off):
    iterations = len(pos_list[0]) - cut_off
    omegas = np.fft.fftfreq(iterations, d=1)
    omegas = np.fft.fftshift(omegas) * np.pi * 2

    S = np.zeros(iterations)

    for pos in pos_list:
        # Compute the Fourier transform for x and y positions
        fft_x_squared = abs(
            np.fft.fftshift(
                np.fft.fft(pos.transpose()[0][cut_off:] - np.average(pos.transpose()[0][cut_off:]))
            )
        ) ** 2
        fft_y_squared = abs(
            np.fft.fftshift(
                np.fft.fft(pos.transpose()[1][cut_off:] - np.average(pos.transpose()[1][cut_off:]))
            )
        ) ** 2

        # Sum the Fourier transforms
        S += fft_x_squared + fft_y_squared

    # Normalize to account for dimensions and number of particles
    fft = np.sqrt(S / (2 * len(pos_list)))
    return omegas, fft

#This coverts into complex numbers unlike the last F
def F2(pos_list, cut_off):
    iterations = len(pos_list[0]) - cut_off
    omegas = np.fft.fftfreq(iterations, d=1)
    omegas = np.fft.fftshift(omegas) * np.pi * 2

    S = np.zeros(iterations)

    for pos in pos_list:
        # Compute the Fourier transform for x and y positions
        x=pos.transpose()[0][cut_off:] - np.average(pos.transpose()[0][cut_off:])
        y=pos.transpose()[1][cut_off:] - np.average(pos.transpose()[1][cut_off:])
        fft=np.fft.fftshift(np.fft.fft(x+y*1j))
        # Sum the Fourier transforms
        S +=abs(fft)**2 

    # Normalize to account for dimensions and number of particles
    fft = S / (2 * len(pos_list))
    return omegas, fft

def identify_peak(fft, omegas):
    max_index = np.argmax(fft)
    return abs(omegas[max_index])




