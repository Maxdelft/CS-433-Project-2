"""
Spyder Editor
This program reads _deletedstray.txt files in each scene folder and calculates glare metrics, then outputs in a _glaremetrics.txt file with one glare metric hdr per row.

Written by: Geraldine Quek
Last edited: 17/11/2021

input: directory of folders of _deletedstray.txt files
output: calculates glare metrics for each scene, and outputs them in a consolidated _glaremetrics.txt file with one row per hdr (p1s1_glaremetrics.txt) for each scene
"""
import os, sys
import subprocess
import math



#expt_1 = 'G:\\My Drive\\PhD\\03 Experiments\\1.1 Low-light Study\\Results\\Measurements\\HDR-LMK_processed\\OnePerScene\\' #####CHANGE INPUT#####
#os.chdir(expt_1)

expt_2a = 'G:\\My Drive\\PhD\\03 Experiments\\2.2 LL Study 2\\Results\\HDRs\\A\\aft\\calib\\'
os.chdir(expt_2a) ##CHANGE ACCORDINGLY##


        
for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_glaremetrics.txt'):
        os.remove(txtfile)

for txtfile in os.listdir(os.getcwd()):
    if txtfile.endswith('_deletedstray.txt'):
        #Make glaremetricsfile
        glaremetricsfile = open((os.path.splitext(txtfile)[0] + '_glaremetrics.txt'), 'w')
        glaremetricsfile.write('participant,ev,edir,eindir,log_gc,dgp,cgi,dgi,dgi_mod,av_lum,med_lum,ugr,ugp,ugr_exp,av_lum_cie')
        glaremetricsfile.write('\n')
        p1 = txtfile.split('s')[0]
        p = p1.split('a')[1] #change 'p' to 'a' for experiment 2A
        print(p)
        ftmp = open(os.path.join(os.getcwd(), txtfile), 'r')
        loggc_list =[]
        glaremetriclist = []
        cgi_loglist = []
        dgi_loglist = []
        dgi_mod_loglist = []
        ugr_exp_loglist = []
        count = 0
        for (num, line) in enumerate(ftmp):
            pieces = line.rstrip().split(' ')
            if pieces[0] == 'dgp,av_lum,E_v,lum_backg,E_v_dir,dgi,ugr,vcp,cgi,lum_sources,omega_sources,Lveil,Lveil_cie,dgr,ugp,ugr_exp,dgi_mod,av_lum_pos,av_lum_pos2,med_lum,med_lum_pos,med_lum_pos2,ugp2:':
                av_lum = pieces[2]
                ev = float(pieces[3])
                med_lum = pieces[20]
            elif num > 0: #line 0 is the header -- (1 No pixels x-pos y-pos L_s Omega_s Posindx L_b L_t E_vert Edir Max_Lum Sigma xdir ydir zdir Eglare_cie Lveil_cie teta glare_zone)
                filename = os.path.splitext(txtfile)[0]
                ev = float(pieces[9]) #E_vert
                ls = float(pieces[4]) #Ls
                omega = float(pieces[5]) #omega solid angle in steradians
                pos = float(pieces[6]) #position index
                bigomega = omega/(pos**2) #for DGI
                edir = float(pieces[10]) #direct illuminance for CGI
                lb = float(pieces[7]) #background luminance
                eindir = math.pi*lb #for CGI
                loggc_t1 = (ls**2)*omega
                loggc_t2 = ev**1.87
                loggc_t3 = pos**2
                loggc= loggc_t1/(loggc_t2*loggc_t3) #summation term in loggc
                loggc_list.append(loggc)#square of luminance of source multiplied by omega (solid angle of source)
                
                cgi_log = ((ls**2)*omega)/(pos**2) #log term in cgi
                cgi_loglist.append(cgi_log)
                dgi_log = ((ls**1.6)*(bigomega**0.8))/(lb + (0.07*(omega**0.5)*ls))
                dgi_loglist.append(dgi_log)
                av_lum_cie = ev/math.pi
                dgi_mod_log = ((ls**1.6)*(bigomega**0.8))/(av_lum_cie**0.85 + (0.07*(omega**0.5)*ls))
                dgi_mod_loglist.append(dgi_mod_log)
                ugr_exp_log = (ls*omega)/(lb*(pos**2))
                ugr_exp_loglist.append(ugr_exp_log)
                
                count += 1 
            
        #participant
        glaremetriclist.append(p)
        print('p='+str(p))
        #ev
        glaremetriclist.append(ev)
        print('Ev='+str(ev))
        #edir
        glaremetriclist.append(edir)
        print('edir='+str(edir))
        #eindir
        glaremetriclist.append(eindir)
        print('eindir='+str(eindir))
        #loggc
        log_gc = math.log10(1 + sum(loggc_list))
        glaremetriclist.append(log_gc)
        print('log_gc='+str(log_gc))
        #DGP
        dgp_c1 = 5.87*(10**-5)
        dgp_c2 = 9.18*(10**-2)
        dgp_c3 = 0.16
        dgp = dgp_c1*ev + dgp_c2*log_gc + dgp_c3
        print('DGP='+str(dgp))
        glaremetriclist.append(dgp)
        #CGI
        cgi_t1 = (1+(edir/500))/ev
        cgi_t2 = sum(cgi_loglist)
        cgi_t3 = 2*cgi_t1*cgi_t2
        if cgi_t3 <= 0:
            cgi = 0
        else: 
            cgi = 8*math.log10(cgi_t3)
        print('CGI='+str(cgi))
        glaremetriclist.append(cgi)
        #DGI
        dgi_t1 = sum(dgi_loglist)
        if dgi_t1 > 0:
            dgi = 10*math.log10(0.478*dgi_t1)
        else: 
            dgi = 0
        print('DGI='+str(dgi))
        glaremetriclist.append(dgi)
        #DGImod
        dgi_mod_t1 = sum(dgi_mod_loglist)
        if dgi_mod_t1 > 0:
            dgi_mod = 10*math.log10(0.478*dgi_mod_t1)
        else: 
            dgi_mod = 0
        print('DGI_mod='+str(dgi_mod))
        glaremetriclist.append(dgi_mod)
        #Average lum (mathematical average)
        glaremetriclist.append(av_lum)
        print('Av_lum='+str(av_lum))
        #median luminance 
        glaremetriclist.append(med_lum)
        print('Med_lum='+str(med_lum))
        #UGR
        ugr_t1 = 0.25/lb
        ugr_t2 = sum(cgi_loglist)
        if ugr_t2 != 0:
            ugr = 8*math.log10(ugr_t1*ugr_t2)
        else:
            ugr = 0
        glaremetriclist.append(ugr)
        print('UGR='+str(ugr))
        #UGP
        if sum(cgi_loglist) != 0:
            ugp_t1 =((1/lb)*(sum(cgi_loglist)))**(-1/5)
            ugp_t2 = 1 + (2/7)*(ugp_t1)
            ugp = 1/(ugp_t2**10)
        else: 
            ugp = 0
        print('UGP='+str(ugp))
        glaremetriclist.append(ugp)
        #UGR_exp
        ugr_exp_t1 = sum(ugr_exp_loglist)
        if ugr_exp_t1 != 0:
            ugr_exp = 8*math.log10(av_lum_cie) + (8*math.log10(ugr_exp_t1))
        else:
            ugr_exp = 0
        print('UGR_exp='+str(ugr_exp))
        glaremetriclist.append(ugr_exp)
        #Av lum CIE (Ev/pi)
        print('Av_lum_cie='+str(av_lum_cie))
        glaremetriclist.append(av_lum_cie)

        print(glaremetriclist)
        glaremetricsfile.write(','.join(str(v) for v in glaremetriclist))
        glaremetricsfile.write('\n')

        glaremetricsfile.close()
        ftmp.close()

                
                
                