#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 21:57:33 2021
This file takes as an input the excel files where the answers are saved if discomfort is experienced.
Those answers are stored as yes/no and they are translated to 1/0.
The translation is stored in Y_2A_bin.
"""

from sklearn.feature_selection import SelectKBest
import pandas as pd
import os,sys
import numpy as np

feature_path    = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A'
X_2A            = np.load("/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A/Arrays/X_2A.npy")
image_names_2A  = np.load("/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A/Arrays/image_names_2A.npy")
results         = pd.read_excel (r'/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Excel_Sheets/results_v211118_CS433.xlsx')
#%% Extract needed data from excel table:
answers     = pd.DataFrame(results, columns= ['Are you experiencing any discomfort due to glare at the moment?']).to_numpy()
store_index = pd.DataFrame(results, columns = ['index']).to_numpy()
part_index  = pd.DataFrame(results, columns = ['Participant Index'])

# Translate answer to binary answer:
answer_bin = translate_answers(answers)
Y_2A_bin   = create_bin_Y(image_names_2A,answer_bin,store_index)
#%%  This function
def create_bin_Y(image_names,answer_bin,store_index):
    # input : image_names : image_names belonging to considered experiment 
    #         answer_bin  : binarary answers of all answers listed in excel
    #         store_index : image names of all images listed in excel
    # output: Y_bin       : binary answers of images considered in the experiment
    Y_bin = np.array([])
    for j in range(len(image_names)):
        Y_string = image_names[j]
        count = 0
        for i in store_index:
            if Y_string[:-4] in str(i):
                Y_bin = np.append(Y_bin, answer_bin[count])
                break
            count += 1
    return Y_bin        
#%% This function translates a 'Yes' to 1 and a 'No' to 0
def translate_answers(answers):
    # input: answers in Yes/No format 
    # output: answers in 1/0 format
    answer_bin = np.array([]);
    for answer in answers:
        if answer == 'Yes':
            answer_bin = np.append(answer_bin,1)
        else:
            answer_bin = np.append(answer_bin,0)
    return answer_bin