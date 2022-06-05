#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:39:41 2022

@author: Alice
"""

# Code to define the classes used in the Assignment 2

class Cluster:
    # This class is used in the k-means algorithm to crate new clusters, each time that k changes
    # the attributes will be explained as follows:
    # centroids: a list that will contain the coordinates (voltage vagnitude and angle)
    # of the centroids of the cluster
    # points_inside: list of the coordinates of the points assigned to that cluster
    # points_inside_mag: list of the voltage magnitudes of all the points assigned to that cluster
    # points_inside_deg: list of the voltage angles of all the points assigned to that cluster
    # label_list: list of the label of all the points assigned to that cluster
    # final_label: the most common lable in the list
    
    def __init__(self, centroids=[], points_inside=[], points_inside_mag=[], points_inside_deg=[],
                 label_list=[], final_label=None):
        self.centroids = centroids
        self.points_inside = points_inside
        self.points_inside_mag = points_inside_mag
        self.points_inside_deg = points_inside_deg
        self.label_list = label_list
        self.final_label = final_label

        
class PointKNN:
    # This class is used in the k-NN algorithm to crate a point for each loop
    # the attributes will be explained as follows:
    # coordinates: array containing the point coordinates
    # label_o: the original label, assigned depending on the state of the grid
    # label_p: label assigned following the k-NN algorithm method
    
    def __init__(self, coordinates=[],label_o = None, label_p = None):
        self.coordinates = []
        self.label_o = label_o
        self.label_p = label_p

class PointsTraining:
    # This class is used in the k-NN algorithm to have a memory
    # regarding all the points in the training set.
    # The attributes will be explained as follows:
    # p_coordinates: to remember the coordinates of the points
    # p_label: to remember the label of the points
    
    def __init__(self, p_coordinates=[], p_label=[]):
        self.p_coordinates = p_coordinates
        self.p_label = p_label
        
    