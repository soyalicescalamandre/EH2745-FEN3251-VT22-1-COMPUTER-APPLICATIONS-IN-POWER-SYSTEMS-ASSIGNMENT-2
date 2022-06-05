#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:03:48 2022

@author: Alice
"""
# Importing all the necessary modules
# the ones important to highlight are:
# m_validation_tot from dscreation_A2 to have the validation data points
# all_t_point will contain the coordinates and the corresponding labels
# of all the training dataset
# classes_A2 in order to use specific classes
# Counter from collections in order to find the most common lable

from dscreation_A2 import m_validation_tot, all_t_point
import numpy as np
import classes_A2 as cA2
from collections import Counter

from tkinter import *
from tkinter import ttk
root = Tk()
root.title('Try k-NN algorithm by yourself')
root.geometry('350x200')

# Creating a Label Widget
explain_label = Label(root, text="This is a k-NN algorithm").grid(row=0, column=1)


def delete():
    message_label.destroy()
    k_input.delete(0,'end')
    submit_btn['state'] = NORMAL

# Function that will allow to try the k-NN method with a value given by the user
def submit():
    global message_label
    k_new = k_input.get()
    def get_distance(d_list):
        return d_list.get('Distance')

    if k_new.startswith('-') and k_new[1:].isdigit():
        message_label = Label(root, text='You should put a positive number\ngrater than 0')
        message_label.grid(row=2, column=1)
    elif k_new.isdigit():
        # Initialize the variables
        # k is taken from the input given in the GUI
        # count is to calculate the accuracy
        # of all the points in the training data
        k = int(k_new)
        if k == 0:
            message_label = Label(root, text='You should put a positive number\ngrather then 0')
            message_label.grid(row=2, column=1)
            submit_btn['state'] = DISABLED
        else:
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
                        count +=1
    
            # Print the result
            # the accuracy is defined as the ratio between the "well" assigned labels
            # and the total number of points in the set
            message_label = Label(root, text='The accuracy with '+ str(k) + '\nis ' + str((count/((r+1)*(c-1)))*100)+'%')
            message_label.grid(row=2, column=1)
            submit_btn['state'] = DISABLED
    else:
        message_label = Label(root, text='You should put a positive number\ngrather then 0')
        message_label.grid(row=2, column=1)
        submit_btn['state'] = DISABLED
    
        
    

# Create the text box
k_input = Entry(root, width=20)
k_input.grid(row=1, column=1)
k_input.insert(0, 'Decide the k you want to use')

# Create the text boxes labels
k_input_label = Label(root, text="New k value")
k_input_label.grid(row=1, column=0)

#Create a Submit button
submit_btn = Button(root, text='Try', command=submit)
submit_btn.grid(row=1, column=3) 

# Delet the message
message_del_btn = Button(root, text='Delete the message', command=delete)
message_del_btn.grid(row=3, column=1) 


root.mainloop()

