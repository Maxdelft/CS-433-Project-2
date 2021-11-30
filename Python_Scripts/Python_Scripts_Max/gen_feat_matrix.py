#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 21:57:33 2021

@author: maximilianvanamerongen
"""

from sklearn.feature_selection import SelectKBest
import pandas as pd
import os,sys
import numpy as np

feature_path = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A'
X_2A = np.load("/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A/Arrays/X_2A.npy")
Y_2A = np.load("/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A/Arrays/Y_2A.npy")
results = pd.read_excel (r'/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Excel_Sheets/results_v211118_CS433.xlsx')

#%%

answers     = pd.DataFrame(results, columns= ['Are you experiencing any discomfort due to glare at the moment?']).to_numpy()
store_index = pd.DataFrame(results, columns = ['index']).to_numpy()
part_index  = pd.DataFrame(results, columns = ['Participant Index'])

answer_bin = translate_answers(answers)
Y_2A_bin   = create_bin_Y(Y_2A,answer_bin,store_index)

    
#%%  
def create_bin_Y(Y_label,answer_bin,store_index):
    Y_bin = np.array([])
    for j in range(len(Y_label)):
        Y_string = Y_label[j]
        count = 0
        for i in store_index:
            if Y_string[:-4] in str(i):
                Y_bin = np.append(Y_bin, answer_bin[count])
                break
            count += 1
    return Y_bin        
#%%

def translate_answers(answers):
    answer_bin = np.array([]);
    for answer in answers:
        if answer == 'Yes':
            answer_bin = np.append(answer_bin,1)
        else:
            answer_bin = np.append(answer_bin,0)
    return answer_bin