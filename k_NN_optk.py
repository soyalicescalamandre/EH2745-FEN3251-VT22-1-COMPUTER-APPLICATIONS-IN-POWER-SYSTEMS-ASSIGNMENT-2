#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 13:11:14 2022

@author: Alice
"""

from dscreation_A2 import m_validation_tot, all_t_point
import numpy as np
import classes_A2 as cA2
from collections import Counter
from k_means import opt_k

def get_distance(d_list):
    return d_list.get('Distance')

# Initialize the variables
# k is taken from the k-mans algorithm
# count is to calculate the accuracy
# sect_training depends on how the training matrix was created
# all_t_point will contain the coordinates and the corresponding labels
# of all the points in the training data
k = opt_k
count = 0

# Memorize the label and the corrispondent coordinates

# k-NN algorithm
# going through all the validation set
# we assign a label to each point dependin on the k nearest neighbors 
for r in range(0, len(m_validation_tot)):
    for c in range(2,10):
        distances = []
        
        point = cA2.PointKNN()
        point.coordinates.append(m_validation_tot[r,c])
        point.coordinates.append(m_validation_tot[r,c+10])
        
        # Assign the original label
        if r in range(0,10):
            point.label_o = 'Default'
        elif r in range(10,20):
            point.label_o = 'Generator disconnected'
            #point.label_o = 'High load'
        elif r in range(20,30):
            point.label_o = 'High load'
            #point.label_o = 'Low load'
        elif r in range(30,40):
            point.label_o = 'Low load'
        else:
            print('something wrong')
        
        # Calculate the distance between the point and all the points in the training set
        # append the value of the distance and the corresponding label to a list of dictionaries
        for t_p in range(len(all_t_point.p_coordinates)):
            dist = np.linalg.norm(np.array(point.coordinates) - np.array(all_t_point.p_coordinates[t_p]))
            distances.append({'Distance' : dist, 'Label': all_t_point.p_label[t_p]})
        
        # Sort in ascending order depending on the distance
        # create a new list that only contains the first k elements
        # initialize the list that will contain the labels of the k nearest neighbors 
        distances.sort(key=get_distance)
        neighbours = distances[:k]
        n_labels = []
        
        # Assign a new label according to the most frequent one in the k neighbors
        # if the assigned label and the original one are the same,
        # increase the counter by one
        for n in neighbours:
            label = n.get('Label')
            n_labels.append(label)
        n_labels2 = Counter(n_labels)
        point.label_p = n_labels2.most_common(1)[0][0]
        if point.label_p == point.label_o:
            count += 1

# Print the result
# the accuracy is defined as the ratio between the "well" assigned labels
# and the total number of points in the set

print("Accuracy with a k value of", k, "is: ", (count/((r+1)*(c-1)))*100, "%")