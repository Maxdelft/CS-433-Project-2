#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 10:36:44 2021

@author: maximilianvanamerongen

This scripts calculates all different log gc values, and stores the created features in X.
All the different features are also stored in txtfiles with the name : 'image_name' + _artfeatures.txt  
The different exponents combinations are saved in the exponents file.
The belonging images names are stored in images_names .

"""

import os, sys
import subprocess
import math
import numpy as np

#%% Define different bounds and the number of exponents you want to iterate through: 

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
expt_2a     = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A'             # Location where all your images are stored
path_2a_art = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2-local/Data/Expt_2A/Artfeatures' # Location where you want to store the txtfile with the different calculated features
os.chdir(expt_2a)

X                = np.zeros((1,10000)) # store feature combinations in this list
image_names      = [];                 # store image names in this list 
features_arr     = []; 

for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_deletedstray.txt'):
        ftmp                 = open(os.path.join(os.getcwd(), txtfile), 'r')
        artfeature_file     = open( os.path.join(path_2a_art,(txtfile + '_artfeatures.txt')),'w')
        
        exponents_list = np.array([]);
        loggc_row    = np.array([]) 
        
        for l in exp_ev_list:              # iterate through different exponents for ev
            for k in exp_omega_list:       # iterate through different exponents for omega
                for j in exp_pos_list:     # iterate through different exponents for pos
                    for i in exp_ls_list:  # iterate through different exponents for ls
                        loggc_list = []
                        exponents_list = np.append(exponents_list,np.array([i,j,k,l]))
            
                        ftmp                 = open(os.path.join(os.getcwd(), txtfile), 'r')
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
                                
                                # Set values for different exponents:
                                exp_ls    = i
                                exp_pos   = j
                                exp_ev    = l
                                exp_omega = k
                                
                                # Calculate different loggc terms 
                                loggc_t1 = (ls**exp_ls)*omega**exp_omega 
                                loggc_t2 = ev**exp_ev
                                loggc_t3 = pos**exp_pos
                                
                                # Calculate and store loggc for every glaresource in the image
                                loggc    = loggc_t1/(loggc_t2*loggc_t3) # summation term in loggc
                                loggc_list.append(loggc)                # square of luminance of source multiplied by omega (solid angle of source)
                               
                                count += 1
                                
                        if loggc_list != []: # Calculate loggc of the image 
                            log_gc    = math.log10(1 + sum(loggc_list))
                            loggc_row = np.append(loggc_row,log_gc)
                
        if loggc_row != []:
            loggc_row = loggc_row.reshape(-1,10) 
            content = str(loggc_row) 
            artfeature_file_tmp.write(','.join(str(v) for v in loggc_row)) # Store calculate features in txtfile
            
            print('loggc row:=',loggc_row) 
            X = np.append(X,np.reshape(loggc_row,(1,-1)),axis = 0) # Store calcualted features in feature matrix X
            image_names.append(txtfile)                            # Store belonging image names in image_names vector 

#%% Process and store calculated feature matrix:
    
X = np.delete(X,0,0) # Delte the first row of zeros

# Store different combinations of exponents in exponents file:
exponents     = open(os.path.join(path_2a_art,'exponents.txt'),'w')
exponents_tmp = open(os.path.join(path_2a_art,'exponents.txt'), 'a')

exponents_tmp.write('ls,pos,omega,ls')
exponents_tmp.write('\n') 
exponents_list = exponents_list.reshape(-1,4)
exponents_tmp.write(','.join(str(v) for v in exponents_list))
#%% Store feature matrix X and images name vector :
np.save("X_2A.npy", X)
np.save("image_names_2A.npy", image_names)