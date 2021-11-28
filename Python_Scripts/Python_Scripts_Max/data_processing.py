#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 11:38:07 2021

@author: maximilianvanamerongen
"""

'Next step: Generate a lot of features ...'


import os, sys
import subprocess
import math


# Deifne directory where data is saved:
expt_2a = '/Users/maximilianvanamerongen/Documents/Master/EPFL/Machine_Learning_CS433/Project2/CS-433-Project-2/Data/Expt_2A'
os.chdir(expt_2a)

for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_glaremetrics.txt'):
        os.remove(txtfile)
        
        
for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_deletedstray.txt'):
        #Make glaremetricsfile
        glaremetricsfile = open((os.path.splitext(txtfile)[0] + '_glaremetrics.txt'), 'w')
        glaremetricsfile.write('participant,ev,omega_list,pos_list,ls_list')
        glaremetricsfile.write('\n')
        p1 = txtfile.split('s')[0]
        p = p1.split('a')[1] #change 'p' to 'a' for experiment 2A
        print(p)
        ftmp = open(os.path.join(os.getcwd(), txtfile), 'r')
        
        loggc_list = []
        omega_list = []
        pos_list   = [] 
        ls_list    = []
        ev_list    = []
        glaremetriclist = []
        p_list          = []
     
        count = 0
        for (num, line) in enumerate(ftmp):
            pieces = line.rstrip().split(' ')
            if pieces[0] == 'dgp,av_lum,E_v,lum_backg,E_v_dir,dgi,ugr,vcp,cgi,lum_sources,omega_sources,Lveil,Lveil_cie,dgr,ugp,ugr_exp,dgi_mod,av_lum_pos,av_lum_pos2,med_lum,med_lum_pos,med_lum_pos2,ugp2:':
                av_lum = pieces[2]
                ev = float(pieces[3])
                med_lum = pieces[20]
            elif num > 0: #line 0 is the header -- (1 No pixels x-pos y-pos L_s Omega_s Posindx L_b L_t E_vert Edir Max_Lum Sigma xdir ydir zdir Eglare_cie Lveil_cie teta glare_zone)
                filename = os.path.splitext(txtfile)[0]
                ev = float(pieces[9])    #E_vert
                ls = float(pieces[4])    #Ls
                omega = float(pieces[5]) #omega solid angle in steradians
                pos   = float(pieces[6])   #position index
                loggc_t1 = (ls**2)*omega
                loggc_t2 = ev**1.87
                loggc_t3 = pos**2
                loggc    = loggc_t1/(loggc_t2*loggc_t3) # summation term in loggc
                loggc_list.append(loggc)                # square of luminance of source multiplied by omega (solid angle of source)
                
                omega_list.append(omega)
                pos_list.append(pos)
                ls_list.append(ls)

                av_lum_cie = ev/math.pi
                
                count += 1 
        
        ev_list.append(ev)
        p_list.append(p)
        
        #participant
        glaremetriclist.append(p_list)
        print('p_list ='+str(p))
        #ev
        glaremetriclist.append(ev_list)
        print('Ev list='+str(ev_list))
        #edir
        glaremetriclist.append(omega_list)
        print('Omega List='+str(omega_list))
        #eindir
        glaremetriclist.append(pos_list)
        print('Pos List='+str(pos_list))
        
        glaremetriclist.append(ls_list)
        print('Ls list='+str(ls_list))
        #DGP
       
        print(glaremetriclist)
        #glaremetricsfile.write(','.join(str(v) for v in glaremetriclist))
        #glaremetricsfile.write('\n')

        glaremetricsfile.close()
        ftmp.close()
        
        
        
        glaremetriclist.append(p)
    print('p='+str(p))
    #ev
    glaremetriclist.append(ev)
    print('Ev='+str(ev))
    #edir
    glaremetriclist.append(ls)
    print('edir='+str(ls))
    #eindir
    glaremetriclist.append(omega)
    print('eindir='+str(omega))
    #eindir
    glaremetriclist.append(pos)
    print('eindir='+str(pos))
    # 
    glaremetriclist.append(pos)
    print('eindir='+str(pos))
    #loggc
    log_gc = math.log10(1 + sum(loggc_list))
    glaremetriclist.append(log_gc)
    print('log_gc='+str(log_gc))
    # 
    glaremetriclist.append(exp_ev)
    print('eindir='+str(exp_ev))
    # 
    glaremetriclist.append(exp_ls)
    print('eindir='+str(exp_ls))
        
    glaremetriclist.append(exp_pos)
    print('eindir='+str(exp_pos))
        
    glaremetriclist.append(bias)
    print('eindir='+str(bias))
        
    #glaremetricsfile.write(','.join(str(v) for v in glaremetriclist))
    glaremetricsfile.write('\n')