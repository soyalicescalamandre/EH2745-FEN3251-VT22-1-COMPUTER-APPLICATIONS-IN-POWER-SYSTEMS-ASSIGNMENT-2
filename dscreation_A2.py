#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:51:18 2022

@author: Alice
"""

# Importing all the necessary modules
import numpy as np
import pandas as pd
import pandapower as pp
import pandapower.control as control
import pandapower.timeseries as timeseries
from pandapower.timeseries.data_sources.frame_data import DFData
import classes_A2 as cA2
import sys


# Definition of the network in pandapower

# Creation of the empty net
net = pp.create_empty_network()

# Creation of buses (b1 is a slack bus)
b1 = pp.create_bus(net, 110)
b2 = pp.create_bus(net, 110)
b3 = pp.create_bus(net, 110)
b4 = pp.create_bus(net, 110)
b5 = pp.create_bus(net, 110)
b6 = pp.create_bus(net, 110)
b7 = pp.create_bus(net, 110)
b8 = pp.create_bus(net, 110)
b9 = pp.create_bus(net, 110)

# Creation of loads
load1 = pp.create_load(net, b5, 90, 30)
load2 = pp.create_load(net, b7, 100, 35)
load3 = pp.create_load(net, b9, 125, 50)

# Creation of lines
line1_4 = pp.create_line(net, b1, b4, 10, "149-AL1/24-ST1A 110.0")
line4_5 = pp.create_line(net, b4, b5, 10, "149-AL1/24-ST1A 110.0")
line5_6 = pp.create_line(net, b5, b6, 10, "149-AL1/24-ST1A 110.0")
line6_3 = pp.create_line(net, b6, b3, 10, "149-AL1/24-ST1A 110.0")
line6_7 = pp.create_line(net, b6, b7, 10, "149-AL1/24-ST1A 110.0")
line7_8 = pp.create_line(net, b7, b8, 10, "149-AL1/24-ST1A 110.0")
line8_2 = pp.create_line(net, b8, b2, 10, "149-AL1/24-ST1A 110.0")
line4_9 = pp.create_line(net, b4, b9, 10, "149-AL1/24-ST1A 110.0")
line8_9 = pp.create_line(net, b8, b9, 10, "149-AL1/24-ST1A 110.0")

# Creation of generators
gen1 = pp.create_sgen(net, b1, 0)
gen2 = pp.create_sgen(net, b2, 163)
gen3 = pp.create_sgen(net, b3, 85)

# Creation of external grid (in order to assure that b1 is a slack bus)
pp.create_ext_grid(net, bus=b1, vm_pu=1.0, va_degree=0.0)

# Plot of the grid
from pandapower.plotting import simple_plot
simple_plot(net, plot_gens=True)

# Timeseries simulation
# The number of timesteps is 160 because the different dataframes
# will be divided into 4 section of 40 points each.
# First section: same values as "default";
# second section: disconnect gen3;
# third section: higher active and reactive power in the loads;
# fourth section: lower active and reactive power in the loads.
# sect_training = the number of rows for each different state of the grid
n_ts = 160
p_ts = 40
sect_training = 30

# Creation of data frames divided into 4 sections to have each of them with different features
# Generators:
df_gen_p1 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.sgen.index))),
               index=list(range(p_ts)), columns=net.sgen.index) * net.sgen.p_mw.values
gen_p2 = [net.sgen.p_mw.values[0], net.sgen.p_mw.values[1], 0]
df_gen_p2 = pd.DataFrame(np.ones((p_ts, len(net.sgen.index))),
               index=list(range(p_ts)), columns=net.sgen.index) * gen_p2
df_gen_p3 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.sgen.index))),
                index=list(range(p_ts)), columns=net.sgen.index) * net.sgen.p_mw.values
df_gen_p4 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.sgen.index))),
               index=list(range(p_ts)), columns=net.sgen.index) * net.sgen.p_mw.values
df_gen = pd.concat([df_gen_p1, df_gen_p2, df_gen_p3, df_gen_p4], ignore_index=True)
#df_gen = pd.concat([df_gen_p1, df_gen_p3, df_gen_p4], ignore_index=True)

# creation of datasources for generators
ds_gen = DFData(df_gen)

# initialising ConstControl controller to update values of the generators ("sgen" elements)
# the element_index specifies which elements to update (we pass net.sgen.index -> all sgens in the net)
# the controlled variable is "p_mw"
# the profile_name are the sgen indices 0-N
const_sgen = control.ConstControl(net, element='sgen', element_index=net.sgen.index,
                                  variable='p_mw', data_source=ds_gen, profile_name=net.sgen.index)


# Loads:
# Active power
df_loadsa_p1 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * net.load.p_mw.values
df_loadsa_p2 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * net.load.p_mw.values
high_load_a = np.array([net.load.p_mw.values[0]*2, net.load.p_mw.values[0]*2, net.load.p_mw.values[0]*2])
df_loadsa_p3 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * high_load_a
df_loadsa_p4 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * net.load.p_mw.values * 0.5
df_load_active = pd.concat([df_loadsa_p1, df_loadsa_p2, df_loadsa_p3, df_loadsa_p4],
                           ignore_index=True)
#df_load_active = pd.concat([df_loadsa_p1, df_loadsa_p3, df_loadsa_p4],
#                           ignore_index=True)

# creation of datasources for loads (active power)
ds_load_active = DFData(df_load_active)

# initialising ConstControl controller to update values of the loads
# the element_index specifies which elements to update (we pass net.load.index -> all loads in the net)
# the controlled variable is "p_mw"
# the profile_name are the load indices 0-N
const_loadsa = control.ConstControl(net, element='load', element_index=net.load.index,
                                  variable='p_mw', data_source=ds_load_active, profile_name=net.load.index)
    
# Reactive power
df_loadsr_p1 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * net.load.q_mvar.values
df_loadsr_p2 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * net.load.q_mvar.values
high_load_r = np.array([net.load.q_mvar.values[0]*2, net.load.q_mvar.values[0]*2,
                        net.load.q_mvar.values[0]*2])
df_loadsr_p3 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * high_load_r
df_loadsr_p4 = pd.DataFrame(np.random.normal(1., 0.05, size=(p_ts, len(net.load.index))),
                  index=list(range(p_ts)), columns=net.load.index) * net.load.q_mvar.values * 0.5
df_load_reactive = pd.concat([df_loadsr_p1, df_loadsr_p2, df_loadsr_p3, df_loadsr_p4],
                             ignore_index=True)
#df_load_reactive = pd.concat([df_loadsr_p1, df_loadsr_p3, df_loadsr_p4],
#                             ignore_index=True)

# creation of datasources for loads (active power)
ds_load_reactive = DFData(df_load_reactive)

# the same as just before, only changing the controlled variable to "q_mvar"
const_loadsr = control.ConstControl(net, element='load', element_index=net.load.index,
                                  variable='q_mvar', data_source=ds_load_reactive,
                                  profile_name=net.load.index)

ow = timeseries.OutputWriter(net, output_path="./", output_file_type=".csv")
ow.log_variable('res_bus', 'vm_pu')
ow.log_variable('res_bus', 'va_degree')
timeseries.run_timeseries(net, calculate_voltage_angles=True)

# Transform the .cvs files into numpy matrix,
# therefore, there will be two big matrices, one for the voltage degrees and one for the modules.
# Each of them will be splitted in two, in order to create a traning dataset and a validation one,
# the training has 120 points (30 for each state) and the validation has 40 (10 per each state)
# IMPORTANT: in order to do so it is necessary the path till the documents just created,
# therefore, to make it work, the green line has to be substituted
degrees_matrix = np.genfromtxt(
    '/Users/Alice/Desktop/SMART CITIES/ESC_2122semester2/CA/CA_A2/__pycache__/res_bus/va_degree.csv',
    delimiter=';')
# Extract from thw whole sample, 10 points per state, in order to create a training data
m_training_vd = np.concatenate((degrees_matrix[:31,:], degrees_matrix[41:71,:],
                              degrees_matrix[81:111,:], degrees_matrix[121:151,:]))
m_validation_vd = np.concatenate((degrees_matrix[31:41,:], degrees_matrix[71:81,:],
                              degrees_matrix[111:121,:], degrees_matrix[151:,:]))

#m_training_vd = np.concatenate((degrees_matrix[:31,:], degrees_matrix[41:71,:],
#                              degrees_matrix[81:111,:]))
#m_validation_vd = np.concatenate((degrees_matrix[31:41,:], degrees_matrix[71:81,:],
#                              degrees_matrix[111:,:]))

# IMPORTANT: in order to do so it is necessary the path till the documents just created,
# therefore, to make it work, the green line has to be substituted
module_matrix = np.genfromtxt(
    '/Users/Alice/Desktop/SMART CITIES/ESC_2122semester2/CA/CA_A2/__pycache__/res_bus/vm_pu.csv',
    delimiter=';')
m_training_vm = np.concatenate((module_matrix[:31,:], module_matrix[41:71,:],
                              module_matrix[81:111,:], module_matrix[121:151,:]))
m_validation_vm = np.concatenate((module_matrix[31:41,:], module_matrix[71:81,:],
                             module_matrix[111:121,:], module_matrix[151:,:]))

#m_training_vm = np.concatenate((module_matrix[:31,:], module_matrix[41:71,:],
#                              module_matrix[81:111,:], module_matrix[121:151,:]))
#m_validation_vm = np.concatenate((module_matrix[31:41,:], module_matrix[71:81,:],
#                              module_matrix[111:,:]))


m_training_tot = np.concatenate((m_training_vm, m_training_vd), axis=1)
m_validation_tot = np.concatenate((m_validation_vm, m_validation_vd), axis=1)

# Initialization of the variable
temp_dist = 0

# Loop to calculate the max distance between the origin of the axis and the data
for r in range(1,len(m_training_tot)):
    for c in range(1,len(net.bus.index)):
        xy = [m_training_tot[r,c], m_training_tot[r,c+10]]
        dist = np.linalg.norm(np.zeros(2) - np.array(xy))
        if dist > temp_dist:
            temp_dist = dist

max_distance = temp_dist

all_t_point = cA2.PointsTraining()

for r in range(1,len(m_training_tot)):
    for c in range(1,10):

        all_t_point.p_coordinates.append([m_training_tot[r,c], m_training_tot[r,c+10]])
        
        # Assign the label
        # the ranges are defined depending on how the training matrix was created
        if r in range(1,sect_training+1):
            all_t_point.p_label.append('Default')
        elif r in range(sect_training+1, 2*sect_training+1):
            all_t_point.p_label.append('Generator disconnected')
        elif r in range(2*sect_training+1, 3*sect_training+1):
            all_t_point.p_label.append('High load')
        elif r in range(3*sect_training+1, 4*sect_training+1):
            all_t_point.p_label.append('Low load')
        else:
            print('Something is wrong')
            sys.exit()
