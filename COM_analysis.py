#!/usr/bin/env python

# given a list of domains claculate and compare their centers of mass

import sys
import numpy as np
import math
import matplotlib.pyplot as plt

def get_bodies():
    allbodies = []
    bodyids = []
    bodydeffile = open(sys.argv[1],'r').readlines()
    print('----- body definitions ------\nname    start   end     chain')
    for i in bodydeffile:
        line = i.split()
        print('{0}\t{1}\t{2}\t{3}'.format(line[0],line[1],line[2],line[3]))
        allbodies.append((line[0],range(int(line[1]),int(line[2])),line[3])) #[name,startAA,endAA,chain]
        bodyids.append(line[0])
    print('-----------------------------')
    return(allbodies,bodyids)

def calc_dist(xyz1,xyz2):
    xdif = ((xyz1[0]-xyz2[0])**2)
    ydif = ((xyz1[1]-xyz2[1])**2)
    zdif = ((xyz1[2]-xyz2[2])**2)
    distance = math.sqrt(xdif+ydif+zdif)
    return(distance)

def calculateCOM(pdbdata,AArange,chain):
    '''calculate the calpha center of mass for a set of atoms'''
    x,y,z = [],[],[]
    print len(pdbdata)
    for line in pdbdata:
        if line[0:4] =='ATOM':
            print line
            if int(line[23:26]) in AArange and line[21] == chain and line[13:16] == 'CA ':
                print('x')
                coords = line[31:56].split()
                x.append(float(coords[0]))
                y.append(float(coords[1]))
                z.append(float(coords[2]))    
    centerofmass = [np.mean(x),np.mean(y),np.mean(z)]
    print centerofmass
    return(centerofmass)

def startup():
    if len(sys.argv) < 3:
        sys.exit('''
USAGE: COM_analysis.py <body definition file> <models file>
---
body definition file = four columns text file
body_name       start_AA        end_AA      chain

models file -  text file list of models one per line -  models must be in order of the motion    

---''') 

def calc_COM_diffs(comlist1,comlist2):
    runningtotal = []
    for i in zip(comlist1,comlist2):
        runningtotal.append(calc_dist(i[0],i[1]))
    return(runningtotal)

###### run the program
startup()
allbodies,bodids = get_bodies()
pdbs = open(sys.argv[2],'r').readlines()
COMSdic = {}                #{filename:[COMbody1, COMbody2, ... COMbodyn]}
# get COM for each body in each pdb
for pdbfile in pdbs:
    data = open(pdbfile.replace('\n',''),'r').readlines()
    print len(data)
    pdbbodlist = []
    for i in allbodies:
        bodyrange = range(i[1][0],i[1][-1])
        COM = calculateCOM(data,bodyrange,i[2])
        pdbbodlist.append(COM)
    COMSdic[pdbfile.replace('\n','')] = pdbbodlist
# feed into correlation analysis

print COMSdic
COMSkeys = COMSdic.keys()
COMSkeys.sort()
totalCOMdiffs = {}
bbCOMdiffs = {}
diffsarray = []
for i in COMSkeys:
    diflist = []
    for j in COMSkeys:
        bbCOMdiffs['{0}//{1}'.format(i,j)] = calc_COM_diffs(COMSdic[i],COMSdic[j])
        totalCOMdiffs['{0}//{1}'.format(i,j)] = np.sum(calc_COM_diffs(COMSdic[i],COMSdic[j]))
        diflist.append(np.sum(calc_COM_diffs(COMSdic[i],COMSdic[j])))
    diffsarray.append(diflist)

for i in totalCOMdiffs:
    print i,totalCOMdiffs[i]
for i in bbCOMdiffs:
    print i,bbCOMdiffs[i]

# correlation matric for all of the domains combined 
plt.matshow(diffsarray,cmap='Reds')
data = np.array(diffsarray)
print data.shape
x_pos = np.arange(len(COMSkeys))
plt.xticks(x_pos,COMSkeys,fontsize='xx-small',rotation='vertical')
y_pos = np.arange(len(COMSkeys))
plt.yticks(y_pos,COMSkeys,fontsize='xx-small')
#plt.title('all domains')

for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        if data[y,x] < np.mean(data)+(np.std(data)*0.5):
            color = 'k'
        else:
            color = 'w'
        plt.text(x, y, '%.1f' % data[y, x],
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize='xx-small',
                 color=color)

plt.savefig('all_domains_diffs.png')
plt.close()

# by body correlation matrices

def get_bb_diff(bodyno,comkey):
    bodydiflist = []
    for j in COMSkeys:
        bodydiflist.append(calc_dist(comkey[bodyno],COMSdic[j][bodyno]))
    return(bodydiflist)

def b_cmatrix(nbody):
    bc_difs = []
    for i in COMSkeys:
        bbdiffarray = get_bb_diff(nbody,COMSdic[i])
        bc_difs.append(bbdiffarray)
    plt.matshow(bc_difs,cmap='Reds')
    x_pos = np.arange(len(COMSkeys))
    plt.xticks(x_pos,COMSkeys,fontsize='xx-small',rotation='vertical')
    y_pos = np.arange(len(COMSkeys))
    plt.yticks(y_pos,COMSkeys,fontsize='xx-small')
    #plt.title('{0}'.format(bodids[nbody]),loc='left')
    data = np.array(bc_difs)
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if data[y,x] < np.mean(data)+(np.std(data)*0.5):
                color = 'k'
            else:
                color = 'w'
            plt.text(x, y, '%.1f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize='xx-small',
                     color=color)
    plt.savefig('{0}_diffs.png'.format(bodids[nbody]))
    plt.close()

for i in range(len(bodids)):
    b_cmatrix(i)
    
def write_outbild(name,listofcoms):
    output = open('COMs_{0}.bild'.format(name.split('.')[0]),'w')
    colors = ['red','blue','yellow','green','white','purple']
    n=0
    first = True
    bildout = []
    for i in listofcoms:
        if first == False:
            bildout.append('{0} {1} {2}\n'.format(i[0],i[1],i[2]))
            
        bildout.append('.color {0}\n'.format(colors[n])) 
        bildout.append('.sphere {0} {1} {2} 1.0\n'.format(i[0],i[1],i[2]))
        bildout.append('.v {0} {1} {2} '.format(i[0],i[1],i[2]))
        first = False
        n+=1
    for i in bildout[:-1]:
        output.write(i)
    output.close()
for i in COMSkeys:
    write_outbild(i,COMSdic[i])
        