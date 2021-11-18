# -*- coding: utf-8 -*-
"""
Spyder Editor
This program consolidates basic statistics of the glare metrics for each _glaremetrics.txt files and outputs them in a single .csv with one row per scene 

Written by: Geraldine Quek
Last edited: 18/11/2021

input: _glaremetrics.txt files
output: consolidated_results.txt
"""


import os, sys
import subprocess
import math
import pandas as pd


#expt_1 = 'G:\\My Drive\\PhD\\03 Experiments\\1.1 Low-light Study\\Results\\Measurements\\HDR-LMK_processed\\OnePerScene\\' #####CHANGE INPUT#####
#os.chdir(expt_1)

expt_2a = 'G:\\My Drive\\PhD\\03 Experiments\\2.2 LL Study 2\\Results\\HDRs\\A\\aft\\calib\\'
os.chdir(expt_2a) ##CHANGE ACCORDINGLY##
 
fileList = [] #_glaremetrics.txt file list

fg = open(('consolidated_results'+'.txt'), 'w')
fg.close()
#fg.write('index,dgp,av_lum,E_v,lum_backg,E_v_dir,dgi,ugr,vcp,cgi,lum_sources,omega_sources,Lveil,Lveil_cie,dgr,ugp,ugr_exp,dgi_mod,av_lum_pos,av_lum_pos2,med_lum,med_lum_pos,med_lum_pos2,total_gc')

#append all _glaremetrics.txt file to fileList
for file in os.listdir(os.getcwd()):
    if file.endswith('_glaremetrics.txt'):
        fileList.append(os.path.join(os.getcwd(), file))
        
#open one glaremetrics txt file and generate header
df = pd.read_csv(fileList[0]) #dataframe of the first file just to get the header out
df = df.reset_index(drop=True) #to get the title header
fg = open(('consolidated_results'+'.txt'), 'w')
fg.write('index'+',')
for col in list(df):
    fg.write(col+',')
fg.write('\n')
        
#iterate through files
for filename in fileList:
    rd = open((filename), 'r')
    fg.write(filename+",")
    for (num, line) in enumerate(rd):
        if num > 0:
            fg.write(line)
    rd.close()

fg.close()