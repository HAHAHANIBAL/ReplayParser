#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import os
import re
import csv
from collections import OrderedDict

path=os.path.expanduser('c:/Users/moc/PycharmProjects/Game/output/475880380.log')
subprocess.call(['DotaParser.exe','475880380.dem'])
rep=open(path,'rb')
rep_15=open('replay_15min.txt','w')
criteria=re.compile(r'.*? \((\d+).*?\)\. .*?')

for line in rep:
    m=criteria.search(line)
    if int(m.group(1)) < 16:
        rep_15.write(line)

rep.close()
rep_15.close()


ordered_fieldnames = OrderedDict([('Radiant_Creep_Kill',None),('Dire_Creep_Kill',None),('Radiant_Tower_Damage',None),('Dire_Tower_Damage',None)])
count_creep_rad=0
count_creep_dire=0
count_tower_dmg_rad=0
count_tower_dmg_dire=0

last_hit_dire=re.compile(r'.*?(Radiant Creep dies)\..*?:.(.*).')
last_hit_rad=re.compile(r'.*?(Dire Creep dies)\..*?:.(.*).')
tower_dmg=re.compile(r'.*?deals.(\d+).damage.to.(.*?).Tier.(\d+).*?')
#=re.compile(r'.*?deals.(\d+).*?(Radiant).*?Tier.(\d+).*?')

with open("replay_15min.txt","rb") as fin:
    for line in fin:
        i=tower_dmg.search(line)
        if i!=None:
            if "Dire" in str(i.group(2)):
                count_tower_dmg_rad=count_tower_dmg_rad+int(i.group(1))
            elif "Radiant" in str(i.group(2)):
                count_tower_dmg_dire=count_tower_dmg_dire+int(i.group(1))
        if "Radiant Creep dies" in line:
            count_creep_dire=count_creep_dire+1
        elif "Dire Creep dies" in line:
            count_creep_rad=count_creep_rad+1


with open("count.csv","wb") as fou:
    stat=csv.DictWriter(fou,fieldnames=ordered_fieldnames)
    stat.writeheader()
    stat=csv.writer(fou)
    stat.writerow([count_creep_rad,count_creep_dire,count_tower_dmg_rad,count_tower_dmg_dire])

