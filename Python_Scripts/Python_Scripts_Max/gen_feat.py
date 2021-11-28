#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 10:36:44 2021

@author: maximilianvanamerongen
TO DO: add looping through different exponents
"""

import os, sys
import subprocess
import math
import numpy as np

#%% Generate for each variable different exponents:
n_ev        = 10
min_ev      = -2.5
max_ev      = 2.5
exp_ev_list = np.linspace(min_ev,max_ev,n_ev)

n_omega        = 10
min_omega      = -2.5
max_omega      = 2.5
exp_omega_list = np.linspace(min_omega,max_omega,n_omega)

n_ls        = 10
min_ls      = -2.5
max_ls      = 2.5
exp_ls_list = np.linspace(min_ls,max_ls,n_ls)

n_pos        = 10
min_pos      = -2.5
max_pos      = 2.5
exp_pos_list = np.linspace(min_pos,max_pos,n_pos)

n_bias        = 10
min_bias      = -2.5
max_bias      = 2.5
exp_bias_list = np.linspace(min_bias,max_bias,n_bias)

#%% Deifne directory where data is saved:
expt_2a     = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2/Data/Expt_2A'
path_2a_art = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2/Data/Expt_2A/Artfeatures'
os.chdir(expt_2a)


features_arr     = np.array([]) # Store all different features in this array: 

for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_deletedstray.txt'):
        ftmp                 = open(os.path.join(os.getcwd(), txtfile), 'r')
        #glaremetricsfile_tmp = open('artificial_features.txt', 'a')
        
        artfeature_file     = open( os.path.join(path_2a_art,(txtfile + '_artfeatures.txt')),'w')
        feature_list = np.array([]);
        loggc_row = np.array([]) 
        
        for l in exp_ev_list:
            for k in exp_omega_list:
                for j in exp_pos_list:
                    for i in exp_ls_list:
                        loggc_list = []
                        feature_list = np.append(feature_list,np.array([i,j,k,l]))
            
                        ftmp                 = open(os.path.join(os.getcwd(), txtfile), 'r')
                        #glaremetricsfile_tmp = open('artificial_features.txt', 'a')
                        artfeature_file_tmp  = open(artfeature_file.name,'a')
        
                        glaremetriclist = []
                        count  = 0
                        for (num, line) in enumerate(ftmp):
                            pieces    = line.rstrip().split(' ')
                            if pieces[0] == 'dgp,av_lum,E_v,lum_backg,E_v_dir,dgi,ugr,vcp,cgi,lum_sources,omega_sources,Lveil,Lveil_cie,dgr,ugp,ugr_exp,dgi_mod,av_lum_pos,av_lum_pos2,med_lum,med_lum_pos,med_lum_pos2,ugp2:':
                                av_lum  = pieces[2]
                                ev      = float(pieces[3])
                                med_lum = pieces[20]
                            elif num > 0 : #line 0 is the header -- (1 No pixels x-pos y-pos L_s Omega_s Posindx L_b L_t E_vert Edir Max_Lum Sigma xdir ydir zdir Eglare_cie Lveil_cie teta glare_zone):
                                filename = os.path.splitext(txtfile)[0]
                                # Extracting measurements:
                                ev    = float(pieces[9])   #E_vert
                                ls    = float(pieces[4])   #Ls
                                omega = float(pieces[5])   #omega solid angle in steradians
                                pos   = float(pieces[6])   #position index
                        
                                exp_ls    = i
                                exp_pos   = j
                                exp_ev    = l
                                exp_omega = k
                                
                                
                                loggc_t1 = (ls**exp_ls)*omega**exp_omega
                                loggc_t2 = ev**exp_ev
                                loggc_t3 = pos**exp_pos
                                loggc    = loggc_t1/(loggc_t2*loggc_t3) # summation term in loggc
                                loggc_list.append(loggc)                # square of luminance of source multiplied by omega (solid angle of source)
                                #print('log gc:',loggc)
                                
                                count += 1
                                
                        if loggc_list != []:
                            log_gc    = math.log10(1 + sum(loggc_list))
                            loggc_row =  np.append(loggc_row,log_gc)
            
                
        if loggc_row != []:
            loggc_row = loggc_row.reshape(-1,10) 
            content = str(loggc_row)
            artfeature_file_tmp.write(','.join(str(v) for v in loggc_row))
            #artfeature_file_tmp.write(content) 
            print('loggc row:=',loggc_row) 
            
        glaremetriclist.append(log_gc)
        loggc_arr = np.array(glaremetriclist)
        features_arr =np.append(features_arr,loggc_arr, axis = 0)
        
        glaremetricsfile_tmp.write(','.join(str(v) for v in glaremetriclist))
        glaremetricsfile_tmp.write('\n')



#%%
exponents     = open(os.path.join(path_2a_art,'exponents.txt'),'w')
exponents_tmp = open(os.path.join(path_2a_art,'exponents.txt'), 'a')

#%%
exponents_tmp.write('ls,pos,omega,ls')
exponents_tmp.write('\n') 
feature_list = feature_list.reshape(-1,4)
exponents_tmp.write(','.join(str(v) for v in feature_list))




