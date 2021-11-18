"""
Spyder Editor
This program reads the -d detailed output from evalglare for each txt file and deletes "stray" glare sources (<500** pixels) and updates the background luminance accordingly.


NOTES:
    ** pixel value should be changed depending on what is considered "stray" in dataset.

Written by: Geraldine Quek
Last edited: 17/11/2021

input: directory of folders of detailed output .txt files
output: _deletedstray.txt files with background luminance updated, and last line of evalglare metrics kept.
"""

import os, sys
import subprocess
import math

#input: folder of folders of txt files
#output: creates new txt files of detailed evalglare results with new background luminance (new_lb) calculated from the weighted old background luminance and the stray glare sources with their respective 


#expt_1 = 'G:\\My Drive\\PhD\\03 Experiments\\1.1 Low-light Study\\Results\\Measurements\\HDR-LMK_processed\\OnePerScene\\' #####CHANGE INPUT#####
#os.chdir(expt_1)

expt_2a = 'G:\\My Drive\\PhD\\03 Experiments\\2.2 LL Study 2\\Results\\HDRs\\A\\aft\\calib\\'
os.chdir(expt_2a) ##CHANGE ACCORDINGLY##


for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_deletedstray.txt'):
        os.remove(txtfile)
    elif txtfile.endswith('_glaremetrics.txt'):
        os.remove(txtfile)
    elif txtfile.endswith('_results.txt'):
        os.remove(txtfile)

for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('.txt'):
        newhdrtxt = open(os.path.splitext(txtfile)[0] + '_deletedstray.txt', 'w')
        ftmp = open(txtfile, 'r') #to read the txt file output
        
        firstline = ftmp.readline() #read first line of file
        if len(firstline) != 0:
            #print(firstline)
            pcs = firstline.rstrip().split(' ')
            numsource = pcs[0] #number of glare sources detected
            newhdrtxt.writelines(firstline) #write header
            #if just 1 glare source is detected, then simply write that line in the newhdrtxt file
            if int(numsource) == 1:
                secondline = ftmp.readline()
                print(secondline)
                newhdrtxt.writelines(secondline)
                thirdline = ftmp.readline()
                newhdrtxt.writelines(thirdline)
            
            #if more than 1 glare source is detected, integrate them by change Lb and Wb in first line, then write first line to newhdrtxt file
            elif int(numsource) > 1:
                lw_list = [] #list of weighted luminances by solid angle to add to new Lb
                stray_wb_list = []
                glaresourceslist = [] #will be a nested list
                Ws = 0 #total sum of source omega
                count = 0
                for (num, line) in enumerate(ftmp): #glare source detailed characteristics (1 No pixels x-pos y-pos L_s Omega_s Posindx L_b L_t E_vert Edir Max_Lum Sigma xdir ydir zdir Eglare_cie Lveil_cie teta glare_zone)
                    pieces = line.rstrip().split(' ') #for each of the next lines, split by space
                    #print(pieces[0])
                    if pieces[0] == "dgp,av_lum,E_v,lum_backg,E_v_dir,dgi,ugr,vcp,cgi,lum_sources,omega_sources,Lveil,Lveil_cie,dgr,ugp,ugr_exp,dgi_mod,av_lum_pos,av_lum_pos2,med_lum,med_lum_pos,med_lum_pos2,ugp2:":
                        evalglaremetrics = line
                    else: 
                        #print(pieces[1])
                        if float(pieces[1]) < 500: # if glare source size is less than 500 pixels
                            lw_list.append(float(pieces[4])*float(pieces[5])) #weighted luminance by solid angle (omega)
                            print(pieces[5])
                            stray_wb_list.append(float(pieces[5]))
                            old_Lb = float(pieces[7])
                            count += 1
                        
                        elif float(pieces[1]) >= 500: # if glare source size is more than 500 pixels, there might be 2 because of the 2 half square scenes
                            glaresourceslist.append(pieces) #this is what to print in the main file, but with Lb revised
                            print(glaresourceslist)
                            old_Lb = float(pieces[7])
                            Ws += float(pieces[5])
                            
                print("old_Lb = " + str(old_Lb))        
                old_Wb = 2*math.pi - Ws - sum(stray_wb_list)
                new_Wb = 2*math.pi - Ws
                new_Lb = ((old_Lb*old_Wb) + sum(lw_list))/new_Wb
                print("new_Lb = " + str(new_Lb))
                
                for line in glaresourceslist: #for each of the main glare sources, replace Lb with new Lb and then write to output file
                    print("Appending main glare source with updated Lb")
                    line[7]=new_Lb #replace new Lb 
                    newhdrtxt.write(' '.join(str(v) for v in line))
                    newhdrtxt.write('\n')
                    
            #print last line of glare metrics from evalglare
                newhdrtxt.write(str(evalglaremetrics))
            
        newhdrtxt.close()
        
        ftmp.close()
