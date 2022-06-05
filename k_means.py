#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 19:04:13 2022

@author: Alice
"""

# Importing all the necessary modules
# the ones important to highlight are:
# m_training_tot from dscreation_A2 to have the training data points
# max_distance from dscreation_A2 to have a threshold
# classes_A2 in order to use specific classes
# Counter from collections in order to find the most common lable

from dscreation_A2 import m_training_tot, all_t_point
from dscreation_A2 import max_distance
import numpy as np
import random
import classes_A2 as cA2
from statistics import mean
import copy
from collections import Counter


# Initialization of most of the variables
# j_icv: in order to calculate how effective are the positon of the centroids and the number of clusters
# j_icv_min_list: in this list all the minimun values of J will be appended, in order to select
# the most effective at the end
# optj_memory: in this list the states that present minimum J will be appended
# with state we mean a "picture" of the cluster division
# k_max: the max number of cluster (+1) that will be tried
j_icv = 0
clusters = []
j_icv_min_list = []
optj_memory = []
k_max = 7

# k-means
for k in range(1,k_max):
    
    # Lists that need to be initialized for each lopp
    j_icv_list = []
    temp_memory_list = []
    
    # Creation of a new object from the class Cluster
    # append it to the list of clusters
    new_cluster = cA2.Cluster()
    clusters.append(new_cluster)
    
    # if k is 1 means that there is pnly one cluster and it is not necessary to have a threshold
    # to decde when to stop moving the centroids
    if k == 1:
        # Assign random centroids to begin with
        temp_centr = [random.randint(1, 120), random.randint(1, 9)]
        temp_centr_mag = m_training_tot[temp_centr[0],temp_centr[1]]
        temp_centr_deg = m_training_tot[temp_centr[0],temp_centr[1]+10]
        temp_centr = [temp_centr_mag, temp_centr_deg]
        clusters[0].centroids = temp_centr
        
        # Going through all the points in the training matrix
        for t_p in range(len(all_t_point.p_coordinates)):
                # Append the coordinates of the point to the corresponding
                # attribute of the cluster
                clusters[0].points_inside_mag.append(all_t_point.p_coordinates[t_p][0])
                clusters[0].points_inside_deg.append(all_t_point.p_coordinates[t_p][1])
                clusters[0].points_inside.append(all_t_point.p_coordinates[t_p])
                clusters[0].label_list.append(all_t_point.p_label[t_p])
        
        # Assign new centroid as the mean of the coordinates of the point inside of the cluster
        clusters[0].centroids = [mean(clusters[0].points_inside_mag),
                                 mean(clusters[0].points_inside_deg)] 
        
        # Calculate J
        for p in clusters[0].points_inside:
            j_icv += np.linalg.norm(np.array(p) - np.array(clusters[0].centroids))
        
        # Assign the final label, not really important because this cluster contains all the points,
        # append the value of J in the list of optimal J values
        clusters[0].final_label = 'All the points are inside'
        j_icv_min_list.append(j_icv) 
    

    else:
        # Because the initial centroids are random,
        # the process will be repeated 100 times
        # due to location optimal
        for i in range(1,101):
            temp_centr_list = []
            
            # Assign random initial centroids for each cluster
            # the statement "if" prevent having the same initial points for more than one cluster
            for j in range(k):
                new = 0
                while new == 0:
                    temp_centr = [random.randint(1, 120), random.randint(1, 9)]
                    temp_centr_mag = m_training_tot[temp_centr[0],temp_centr[1]]
                    temp_centr_deg = m_training_tot[temp_centr[0],temp_centr[1]+10]
                    temp_centr = [temp_centr_mag, temp_centr_deg]
                    if temp_centr not in temp_centr_list:
                        new = 1
                        temp_centr_list.append(temp_centr)
                        clusters[j].centroids = temp_centr

            # The while loop will stop when a certain threshold is reached
            # the threshold chosen was 25% of the max difference,
            # defined as the max distance between the origin of the axis and the data.
            # The while loop is necessary in order to move the centroids of each cluster
            flag = 0
            while flag == 0:
                
                # Initialize all the attributes, but the centroids, of each cluster
                for j in range(k):
                    clusters[j].points_inside = []
                    clusters[j].points_inside_deg = []
                    clusters[j].points_inside_mag = []
                    clusters[j].label_list = []
            
                # For each point in the training set
                # we initialize a list call 'distances' that will contain
                # all the distance values from that point to each centroid
                for t_p in range(len(all_t_point.p_coordinates)):
                    distances = []
                    
                    # Calculate the distance between the point and the centroid of each cluster
                    # and at the end append the distance in a list
                    for cl in clusters:
                        dist = np.linalg.norm(np.array(all_t_point.p_coordinates[t_p])
                                              - np.array(cl.centroids))
                        distances.append(dist)
                            
                        # Check if the distance just calculated is the minimum distance
                        # if so, we want to remember the coordinates of the centroid
                        if dist == min(distances):
                            xy_tempcentroids = cl.centroids
                    
                    # Going through all the clusters,
                    # we want to append the point in the correct one,
                    # looking for correspondance in the centroid coordinates
                    for clu in clusters:
                        if xy_tempcentroids == clu.centroids:
                            clu.points_inside_mag.append(all_t_point.p_coordinates[t_p][0])
                            clu.points_inside_deg.append(all_t_point.p_coordinates[t_p][1])
                            clu.points_inside.append(all_t_point.p_coordinates[t_p])
                            clu.label_list.append(all_t_point.p_label[t_p])
                
                # Initialize the flag "dont_move"                 
                dont_move = 0
                
                # For each cluster we assign new centroids coordinates,
                # as the mean of the coordinates of the points inside of each cluster.
                # If the distance between the "old" centroid and the "new" one is
                # less than 25% of the max distance,
                # then the flag dont_move will increase by one
                # If this condition is satisfied for all the centroids, than the while loop
                # will be interrupted
                for clust in clusters:
                    centr_mean = [mean(clust.points_inside_mag), mean(clust.points_inside_deg)]
                    if np.linalg.norm(np.array(clust.centroids)
                                      - np.array(centr_mean)) < 0.25 * max_distance:
                        dont_move += 1 
                        clust.centroids = centr_mean #not sure if it works
                    else:
                        clust.centroids = centr_mean
                if dont_move == len(clusters):
                    flag = 1
              
            # Calculate J and add this value to a list
            # in order to pick the minimum after 100 loops.
            # Also assign a final lable to each cluster,
            # as the most common lable
            for cluster in clusters:  
                counter = Counter(cluster.label_list)
                cluster.final_label = counter.most_common(1)
                for p in cluster.points_inside:
                    j_icv += np.linalg.norm(np.array(p) - np.array(cluster.centroids))
            
            j_icv_list.append(j_icv)
               
            # Initialization of the J value    
            j_icv = 0
        
        # Append the minimum J to j_icv_min_list
        j_icv_min_list.append(min(j_icv_list))  

# Find the optimal number of clusters, using the elbow method.
# The threshold is defined as the 25% od the difference between
# the highest and the second highest J values
max_difference = j_icv_min_list[0]-j_icv_min_list[1]
for s in range(len(j_icv_min_list)):
    if j_icv_min_list[s]-j_icv_min_list[s+1] < max_difference * 0.25:
        opt_k = s+1
        break
# Print the result
print('The optimal number of cluster is:', opt_k)




       
                      