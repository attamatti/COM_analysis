#!/usr/bin/env python

import sys

try:
    bildfiles = sys.argv[1:]
except:
    sys.exit('USAGE: COM_analyse_batch_bilds.py <bild file search string>')

coordsdic = {}              #{filename:[(x1,y1,z1),(x2,y2,z2),...,(xn,yn,zn)]}
for file in bildfiles:
    data = open(file,'r').readlines()
    coordsdic[file] = []
    for i in data:
        line = i.split()
        if line[0] =='.sphere':
            print(line)
            coordsdic[file].append([float(x) for x in line[1:4]])

def calcdist(coords1,coords2):
    running = []
    n=0
    for i in coords1:
        running.append(abs(coords1[n][0]-coords2[n][0])+abs(coords1[n][1]-coords2[n][1])+abs(coords1[n][2]-coords2[n][2]))
        n+=1
    return(sum(running))

combosdic = {}
for c1 in coordsdic:
    for c2 in coordsdic:
        try:
            combosdic[c1][calcdist(coordsdic[c1],coordsdic[c2])]=c2
        except:
            combosdic[c1] = {calcdist(coordsdic[c1],coordsdic[c2]):c2}
#for i in combosdic:
#    print(i)
#    print(combosdic[i])

def returnmin(listofdics):          # listofdics format [{value:name,value:name}]
    LODkeys = [x for x in listofdics]
    LODkeys.sort()
    #print(LODkeys,min(LODkeys),listofdics[min(LODkeys)])
    for i in LODkeys[1:6]:
        print(i,listofdics[i]) 

for i in combosdic:
    print(i)
    returnmin(combosdic[i])