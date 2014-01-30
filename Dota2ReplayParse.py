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
glyph_dire_usage=0
glyph_rad_usage=0
glyph_pat=re.compile(r'.*?\((\d+):\d+\)..Glyph used by (\w+)')

for line in info:
    if "Radiant picks" in line:
        hero_rad.write(str(hero_side.search(line).group(1))+'\n')
        hero_list_dire.append(str(hero_side.search(line).group(1)))
    elif "Dire picks" in line:
        hero_dire.write(str(hero_side.search(line).group(1))+'\n')
        hero_list_rad.append(str(hero_side.search(line).group(1)))
    i=glyph_pat.search(line)
    if i!=None:
        if i.group(2)=='Dire' and int(i.group(1))<16:
            glyph_dire_usage=glyph_dire_usage+1
        elif i.group(2)=='Radiant' and int(i.group(1))<16:
            glyph_rad_usage=glyph_rad_usage+1



hero_rad.close()
hero_dire.close()
#print hero_list_rad
hero_rad_index=[]
hero_dire_index=[]
with open('hero_index.txt','rb') as fin:
    for line in fin:
        if re.compile(r'(\w+).*,(\d+)').search(line).group(1) in hero_list_rad:
            hero_rad_index.append(re.compile(r'(\w+).*,(\d+)').search(line).group(2))
        elif re.compile(r'(\w+).*,(\d+)').search(line).group(1) in hero_list_dire:
            hero_dire_index.append(re.compile(r'(\w+).*,(\d+)').search(line).group(2))

fin.close()

#print hero_rad_index
neutrals_index=[]
fin=open('neutrals_index.txt','rb')
for line in fin:
    neutrals_index.append(line.strip())
fin.close()


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
fin.close()


valid_kills=re.compile(r'\d+:\d+.\(\d+:\d+\)..(.*?).dies..Killer:.(\w+)')

neutral_kills_rad=0
neutral_kills_dire=0
ward_kills_dire=0
ward_kills_rad=0
hero_kills_rad=0
hero_kills_dire=0

valid_kills_hero=re.compile(r'\d+:\d+.\((\d+):(\d+)\)..(\w+).*?dies..Killer:.(\w+)')
rad_kill_time=[]
dire_kill_time=[]

smoke_pat=re.compile(r'.*?\((\d+):(\d+)\)\..(\w+).*?gets the Smoke of Deceit Buff')
smoke_rad_time=0
smoke_dire_time=0
smoke_rad=[]
smoke_dire=[]
with open("replay_15min.txt","rb") as fin:
    for line in fin:
        i=valid_kills.search(line)
        j=valid_kills_hero.search(line)
        k=smoke_pat.search(line)
        if i!=None:
            if i.group(1) in neutrals_index and i.group(2) in hero_list_rad:
                neutral_kills_rad=neutral_kills_rad+1
            elif i.group(1) in neutrals_index and i.group(2) in hero_list_dire:
                neutral_kills_dire=neutral_kills_dire+1
            elif i.group(1) == "Observer Ward" and i.group(2) in hero_list_dire:
                ward_kills_dire=ward_kills_dire+1
            elif i.group(1) == "Observer Ward" and i.group(2) in hero_list_rad:
                ward_kills_rad=ward_kills_rad+1
        if j!=None:
            if j.group(3) in hero_list_dire:
                hero_kills_rad=hero_kills_rad+1
                rad_kill_time.append(int(j.group(1))*60+int(j.group(2)))
            elif j.group(3) in hero_list_rad:
                hero_kills_dire=hero_kills_dire+1
                dire_kill_time.append(int(j.group(1))*60+int(j.group(2)))
        if k!=None:
            if k.group(3) in hero_list_dire:
                smoke_dire.append(int(k.group(1))*60+int(k.group(2)))
            elif k.group(3) in hero_list_rad:
                smoke_rad.append(int(k.group(1))*60+int(k.group(2)))
fin.close()
smoke_counts_dire=len(set(smoke_dire))
smoke_counts_rad=len(set(smoke_rad))
smoke_dire_unique_time=list(set(smoke_dire))[0:3]
smoke_rad_unique_time=list(set(smoke_rad))[0:3]


if rad_kill_time[0]<dire_kill_time[0]:
    first_blood_time=rad_kill_time[0]
    first_blood_rad=1
else:
    first_blood_time=dire_kill_time[0]
    first_blood_rad=0


ordered_fieldnames = OrderedDict([('Radiant_Hero_Kills',None),('Dire_Hero_Kills',None),('Radiant_FB_Bool',None),('Radiant_Creep_Kills',None),('Dire_Creep_Kills',None),('Radiant_Creep_Denies',None),('Dire_Creep_Denies',None),('Smoke_Counts_Radiant',None),('Smoke_Counts_Dire',None),('Glyph_Usage_Radiant',None),('Glyph_Usage_Dire',None),('Radiant_Tower_Damage',None),('Dire_Tower_Damage',None),('Rad_Neutrals_Farmed',None),('Dire_Neutrals_Farmed',None),('Radiant_Ward_Kills',None),('Dire_Ward_Kills',None),('Rad_Hero_1',None),('Rad_Hero_2',None),('Rad_Hero_3',None),('Rad_Hero_4',None),('Rad_Hero_5',None),('Dire_Hero_1',None),('Dire_Hero_2',None),('Dire_Hero_3',None),('Dire_Hero_4',None),('Dire_Hero_5',None)])
with open("count.csv","wb") as fou:
    stat=csv.DictWriter(fou,fieldnames=ordered_fieldnames)
    stat.writeheader()
    stat=csv.writer(fou)
    stat.writerow([hero_kills_rad,hero_kills_dire,first_blood_rad,count_creep_rad_kills,count_creep_dire_kills,count_creep_rad_denies,count_creep_dire_denies,smoke_counts_rad,smoke_counts_dire,glyph_rad_usage,glyph_dire_usage,count_tower_dmg_rad,count_tower_dmg_dire,neutral_kills_rad,neutral_kills_dire,ward_kills_rad,ward_kills_dire,hero_rad_index[0],hero_rad_index[1],hero_rad_index[2],hero_rad_index[3],hero_rad_index[4],hero_dire_index[0],hero_dire_index[1],hero_dire_index[2],hero_dire_index[3],hero_dire_index[4]])

