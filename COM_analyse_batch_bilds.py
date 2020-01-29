#!/usr/bin/env python

# compare bildfiles - return the n number of best matches from all of the tested files
# modified to have a list of files to compare to.


import sys
import matplotlib.pyplot as plt

try:
    bildfiles1 = open(sys.argv[1],'r').readlines()
    bildfiles2 = open(sys.argv[2],'r').readlines()
    nmatch = int(sys.argv[-1])+1
except:
    sys.exit('USAGE: COM_analyse_batch_bilds.py <bildfile list 1> <bildfile list 2> <number of matches to return>')

coordsdic1 = {}              #{filename:[(x1,y1,z1),(x2,y2,z2),...,(xn,yn,zn)]}
for file in bildfiles1:
    data = open(file.replace('\n',''),'r').readlines()
    coordsdic1[file] = []
    for i in data:
        line = i.split()
        if line[0] =='.sphere':
            coordsdic1[file].append([float(x) for x in line[1:4]])

coordsdic2 = {}              #{filename:[(x1,y1,z1),(x2,y2,z2),...,(xn,yn,zn)]}
for file in bildfiles2:
    data = open(file.replace('\n',''),'r').readlines()
    coordsdic2[file] = []
    for i in data:
        line = i.split()
        if line[0] =='.sphere':
            coordsdic2[file].append([float(x) for x in line[1:4]])


def calcdist(coords1,coords2):
    running = []
    n=0
    for i in coords1:
        running.append(abs(coords1[n][0]-coords2[n][0])+abs(coords1[n][1]-coords2[n][1])+abs(coords1[n][2]-coords2[n][2]))
        n+=1
    return(sum(running))

combosdic = {}
for c1 in coordsdic1:
    for c2 in coordsdic2:
        try:
            combosdic[c1][calcdist(coordsdic1[c1],coordsdic2[c2])]=c2
        except:
            combosdic[c1] = {calcdist(coordsdic1[c1],coordsdic2[c2]):c2}

def returnmin(listofdics):          # listofdics format [{value:name,value:name}]
    LODkeys = [x for x in listofdics]
    LODkeys.sort()


for i in combosdic:
    reved = {}
    print('matches for',i)
    returnmin(combosdic[i])
    for j in combosdic[i]:
        reved[combosdic[i][j]] = j
    sortedreversed = sorted(reved.items() , reverse=False, key=lambda x: x[1])
    for j in sortedreversed[1:nmatch]:
        print(j[0],j[1])
    
    # make the graph:
    revkeys = list(reved)
    revkeys.sort()
    sortedvals = []
    for j in revkeys:
        sortedvals.append(reved[j])
    fig, ax = plt.subplots()
    ax.scatter(range(len(bildfiles2)),sortedvals)
    plt.xticks(range(len(revkeys)))
    plt.ylim(bottom=0)
    plt.ylabel('Distance')
    plt.title(i.replace('.bild',''))
    ax.set_xticklabels([x.replace('.bild','') for x in revkeys],fontsize='xx-small',rotation='45',ha='right')
    plt.savefig('{0}_plots.png'.format(i.split('.')[0]))
    plt.tight_layout()
    plt.close()
