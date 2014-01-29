#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import os
import re
import csv
from collections import OrderedDict

matchid=475880380
subprocess.call(['DotaParser.exe','%d.dem' %matchid])

path=os.path.expanduser('c:/Users/moc/PycharmProjects/Game/output/%d.log' %matchid)
path2=os.path.expanduser('c:/Users/moc/PycharmProjects/Game/output/%d.txt' %matchid)
info=open(path2,'rb')
hero_side=re.compile(r'picks (\w+).')

hero_rad=open('hero_rad.txt','w')
hero_dire=open('hero_dire.txt','w')
hero_list_rad=[]
hero_list_dire=[]

for line in info:
    if "Radiant picks" in line:
        hero_rad.write(str(hero_side.search(line).group(1))+'\n')
        hero_list_dire.append(str(hero_side.search(line).group(1)))
    elif "Dire picks" in line:
        hero_dire.write(str(hero_side.search(line).group(1))+'\n')
        hero_list_rad.append(str(hero_side.search(line).group(1)))

hero_rad.close()
hero_dire.close()
#print hero_list_rad

rep=open(path,'rb')
rep_15=open('replay_15min.txt','w')
criteria=re.compile(r'.*? \((\d+).*?\)\. .*?')

for line in rep:
    m=criteria.search(line)
    if int(m.group(1)) < 16:
        rep_15.write(line)

rep.close()
rep_15.close()



count_creep_rad=0
count_creep_dire=0
count_tower_dmg_rad=0
count_tower_dmg_dire=0

last_hit_dire=re.compile(r'.*?(Radiant Creep dies)\..*?:.(\w+)')
last_hit_rad=re.compile(r'.*?(Dire Creep dies)\..*?:.(\w+).')
tower_dmg=re.compile(r'deals.(\d+).damage.to.(\w+).(.*?).Tier.(\d+).Tower.*?Owner:.(\w+)')
#=re.compile(r'.*?deals.(\d+).*?(Radiant).*?Tier.(\d+).*?')

#rad_creep=open('hero_rad.txt','rb')
#dire_creep=open('hero_dire.txt','rb')
count_creep_dire_kills=0
count_creep_rad_kills=0

with open("replay_15min.txt","rb") as fin:
    for line in fin:
        i=tower_dmg.search(line)
        if i!=None:
            if "Dire" in str(i.group(2)):
                count_tower_dmg_rad=count_tower_dmg_rad+int(i.group(1))
            elif "Radiant" in str(i.group(2)):
                count_tower_dmg_dire=count_tower_dmg_dire+int(i.group(1))
        if "Radiant Creep dies" in line:
#            for item in dire_creep:
#            print str(last_hit_dire.search(line).group(2))
            if str(last_hit_dire.search(line).group(2)) in hero_list_dire:
#                print last_hit_dire.search(line).group(2)
                count_creep_dire_kills=count_creep_dire_kills+1
            count_creep_dire=count_creep_dire+1
        elif "Dire Creep dies" in line:
#            for item in rad_creep:
            if str(last_hit_rad.search(line).group(2)) in hero_list_rad:
                count_creep_rad_kills=count_creep_rad_kills+1
            count_creep_rad=count_creep_rad+1

count_creep_rad_denies=count_creep_dire-count_creep_dire_kills
count_creep_dire_denies=count_creep_rad-count_creep_rad_kills


ordered_fieldnames = OrderedDict([('Radiant_Creep_Kills',None),('Dire_Creep_Kills',None),('Radiant_Creep_Denies',None),('Dire_Creep_Denies',None),('Radiant_Tower_Damage',None),('Dire_Tower_Damage',None)])
with open("count.csv","wb") as fou:
    stat=csv.DictWriter(fou,fieldnames=ordered_fieldnames)
    stat.writeheader()
    stat=csv.writer(fou)
    stat.writerow([count_creep_rad_kills,count_creep_dire_kills,count_creep_rad_denies,count_creep_dire_denies,count_tower_dmg_rad,count_tower_dmg_dire])

