#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import os
import re
import csv
from collections import OrderedDict
from Tkinter import *
from itertools import izip_longest
from matplotlib import pyplot
import matplotlib as mpl
import WebAPIInfo

master=Tk()
master.wm_title("DOTA2 Quant")

photo=PhotoImage(file='DOTA2_header.gif')

canvas=Canvas(master,width=350, height=200)
canvas.create_image(175,90,image=photo)
canvas.pack()
e=Entry(master,width=15)
e2=Entry(master,width=15)
w=Label(master, text="Please input your match ID:")
w2=Label(master, text="Please input your desired compile game time:")
#text=Text(master, width=10,height=10)
#text.(END,"Please Input Your Match ID:")
#text.pack()
w.pack()
e.pack()
w2.pack()
e2.pack()
e2.focus_set()
e.focus_set()


ordered_fieldnames = OrderedDict([('Match_ID',None),('Match_Duration',None),('Radiant_Win',None),('Radiant_Hero_Kills',None),('Dire_Hero_Kills',None),('Radiant_Hero_Damages_Dealt',None),('Dire_Hero_Damages_Dealt',None),('Radiant_Hero_Healed',None),('Dire_Hero_Healed',None),('Radiant_FB_Bool',None),('Radiant_Creep_Kills',None),('Dire_Creep_Kills',None),('Radiant_Creep_Denies',None),('Dire_Creep_Denies',None),('Smoke_Counts_Radiant',None),('Smoke_Counts_Dire',None),('Glyph_Usage_Radiant',None),('Glyph_Usage_Dire',None),('Radiant_Tower_Damage',None),('Dire_Tower_Damage',None),('Rad_Neutrals_Farmed',None),('Dire_Neutrals_Farmed',None),('Radiant_Ward_Kills',None),('Dire_Ward_Kills',None),('Rad_Hero_1',None),('Rad_Hero_2',None),('Rad_Hero_3',None),('Rad_Hero_4',None),('Rad_Hero_5',None),('Dire_Hero_1',None),('Dire_Hero_2',None),('Dire_Hero_3',None),('Dire_Hero_4',None),('Dire_Hero_5',None)])
fout=open("count.csv","wb")
stat=csv.DictWriter(fout,fieldnames=ordered_fieldnames)
stat.writeheader()
stat=csv.writer(fout)



def callback():
    matchid=int(e.get())
#   for matchid in range(475880380,475880380):
#   matchid=475880380
    Fetch_info=WebAPIInfo.getmatch(matchid)
    banlist=Fetch_info.hero_bans_names
    #import some other match info from fetching WebAPI function
    match_duration=Fetch_info.duration
    radiant_win_bool=Fetch_info.rad_win_bool
    dire_name=Fetch_info.dire_team
    rad_name=Fetch_info.rad_team
    player_info=Fetch_info.player_dict

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

#    print hero_list_dire
    hero_rad.close()
    hero_dire.close()
    hero_rad_index=[]
    hero_dire_index=[]
    with open('hero_index.txt','rb') as fin:
        for line in fin:
            if re.compile(r'(\w+).*,(\d+)').search(line).group(1) in hero_list_rad:
                hero_rad_index.append(re.compile(r'(\w+).*,(\d+)').search(line).group(2))
            elif re.compile(r'(\w+).*,(\d+)').search(line).group(1) in hero_list_dire:
                hero_dire_index.append(re.compile(r'(\w+).*,(\d+)').search(line).group(2))

    fin.close()

#   hero_dire_dict = dict(izip_longest(*[iter(hero_dire_index)] * 2, fillvalue=""))
#   Hero list is opposite
#   Convert into class attribute later
    hero_dire_dict={};hero_rad_dict={}
    hero_dire_lh={};hero_rad_lh={}
    hero_dire_deny={};hero_rad_deny={}
    hero_dire_heal={};hero_rad_heal={}
    hero_dire_tango={};hero_rad_tango={}
    hero_dire_flask={};hero_rad_flask={}
    hero_dire_bottle={};hero_rad_bottle={}
    hero_dire_kills={};hero_rad_kills={}
    hero_dire_assists={};hero_rad_assists={}
    hero_dire_ward_kill={};hero_rad_ward_kill={}
    hero_dire_die={};hero_rad_die={}
    hero_dire_smoke_part={};hero_rad_smoke_part={}
    hero_dire_rune_get={};hero_rad_rune_get={}
    hero_dire_roshan={};hero_rad_roshan={}
    hero_dire_neutral={};hero_rad_neutral={}

    with open('hero_rad.txt','rb') as fin:
        for line in fin:
            hero_dire_dict[line.strip()]=0
            hero_dire_lh[line.strip()]=0;hero_dire_deny[line.strip()]=0
            hero_dire_heal[line.strip()]=0;hero_dire_tango[line.strip()]=0
            hero_dire_flask[line.strip()]=0;hero_dire_bottle[line.strip()]=0
            hero_dire_kills[line.strip()]=0;hero_dire_die[line.strip()]=0
            hero_dire_assists[line.strip()]=0;hero_dire_ward_kill[line.strip()]=0
            hero_dire_smoke_part[line.strip()]=0;hero_dire_rune_get[line.strip()]=0
            hero_dire_roshan[line.strip()]=0;hero_dire_neutral[line.strip()]=0
    fin.close()

    with open('hero_dire.txt','rb') as fin:
        for line in fin:
            hero_rad_dict[line.strip()]=0
            hero_rad_lh[line.strip()]=0;hero_rad_deny[line.strip()]=0
            hero_rad_heal[line.strip()]=0;hero_rad_tango[line.strip()]=0
            hero_rad_flask[line.strip()]=0;hero_rad_bottle[line.strip()]=0
            hero_rad_kills[line.strip()]=0;hero_rad_die[line.strip()]=0
            hero_rad_assists[line.strip()]=0;hero_rad_ward_kill[line.strip()]=0
            hero_rad_smoke_part[line.strip()]=0;hero_rad_rune_get[line.strip()]=0
            hero_rad_roshan[line.strip()]=0;hero_rad_neutral[line.strip()]=0
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

#   rad_creep=open('hero_rad.txt','rb')
#   dire_creep=open('hero_dire.txt','rb')
    count_creep_dire_kills=0
    count_creep_rad_kills=0
    count_creep_rad_denies=0
    count_creep_dire_denies=0

    with open("replay_15min.txt","rb") as fin:
        for line in fin:
            i=tower_dmg.search(line)
            if i!=None:
                if "Dire" in str(i.group(2)):
                    count_tower_dmg_rad=count_tower_dmg_rad+int(i.group(1))
                elif "Radiant" in str(i.group(2)):
                    count_tower_dmg_dire=count_tower_dmg_dire+int(i.group(1))
            if "Radiant Creep dies" in line:
#               for item in dire_creep:
#               print str(last_hit_dire.search(line).group(2))
                if str(last_hit_dire.search(line).group(2)) in hero_list_dire:
#                   print last_hit_dire.search(line).group(2)
                    count_creep_dire_kills+=1
                    hero_dire_lh[str(last_hit_dire.search(line).group(2))]+=1
                elif str(last_hit_dire.search(line).group(2)) in hero_list_rad:
                    count_creep_rad_denies+=1
                    hero_rad_deny[str(last_hit_dire.search(line).group(2))]+=1
                count_creep_dire+=1
            elif "Dire Creep dies" in line:
#               for item in rad_creep:
                if str(last_hit_rad.search(line).group(2)) in hero_list_rad:
                    count_creep_rad_kills+=1
                    hero_rad_lh[str(last_hit_rad.search(line).group(2))]+=1
                elif str(last_hit_rad.search(line).group(2)) in hero_list_dire:
                    count_creep_dire_denies+=1
                    hero_dire_deny[str(last_hit_rad.search(line).group(2))]+=1
                count_creep_rad+=1


    fin.close()


    valid_kills=re.compile(r'\d+:\d+.\(\d+:\d+\)..(.*?).dies..Killer:.(\w+)')

    neutral_kills_rad=0;neutral_kills_dire=0
    ward_kills_dire=0;ward_kills_rad=0
    hero_kills_rad=0;hero_kills_dire=0
    valid_kills_hero=re.compile(r'\d+:\d+.\((\d+):(\d+)\)..(\w+).*?dies..Killer:.(\w+)')
    rad_kill_time=[];dire_kill_time=[]
    smoke_pat=re.compile(r'.*?\((\d+):(\d+)\)\..(\w+).*?gets the Smoke of Deceit Buff')
    rune_pat=re.compile(r'.*?\((\d+):(\d+)\)\..(\w+).*?gets the (\w+).*?(Rune)')
    rune_rad=0;rune_dire=0
#    smoke_rad_time=0;smoke_dire_time=0
    smoke_rad=[];smoke_dire=[]
    with open("replay_15min.txt","rb") as fin:
        for line in fin:
            i=valid_kills.search(line)
            j=valid_kills_hero.search(line)
            k=smoke_pat.search(line)
            z=rune_pat.search(line)
            if i!=None:
                if i.group(1) in neutrals_index and i.group(2) in hero_list_rad:
                    hero_rad_neutral[i.group(2)]+=1
                    neutral_kills_rad=neutral_kills_rad+1
                elif i.group(1) in neutrals_index and i.group(2) in hero_list_dire:
                    hero_dire_neutral[i.group(2)]+=1
                    neutral_kills_dire=neutral_kills_dire+1
                elif i.group(1) == "Observer Ward" and i.group(2) in hero_list_dire:
                    hero_dire_ward_kill[i.group(2)]+=1
                    ward_kills_dire=ward_kills_dire+1
                elif i.group(1) == "Observer Ward" and i.group(2) in hero_list_rad:
                    hero_rad_ward_kill[i.group(2)]+=1
                    ward_kills_rad=ward_kills_rad+1
            if j!=None:
                #counting valid kills/deaths but not including suicides or denies
                if j.group(3) in hero_list_dire and j.group(4)!=j.group(3) and j.group(4 in hero_list_rad):
                    hero_dire_die[j.group(3)]+=1
                    hero_rad_kills[j.group(4)]+=1
                    hero_kills_rad=hero_kills_rad+1
                    rad_kill_time.append(int(j.group(1))*60+int(j.group(2)))
                elif j.group(3) in hero_list_rad and j.group(4)!=j.group(3) and j.group(4) in hero_list_dire:
                    hero_dire_kills[j.group(4)]+=1
                    hero_rad_die[j.group(3)]+=1
                    hero_kills_dire=hero_kills_dire+1
                    dire_kill_time.append(int(j.group(1))*60+int(j.group(2)))
                #can add suicide and deny counts here
            if k!=None:
                if k.group(3) in hero_list_dire:
                    hero_dire_smoke_part[k.group(3)]+=1
                    smoke_dire.append(int(k.group(1))*60+int(k.group(2)))
                elif k.group(3) in hero_list_rad:
                    hero_rad_smoke_part[k.group(3)]+=1
                    smoke_rad.append(int(k.group(1))*60+int(k.group(2)))
            if z!=None:
                if z.group(3) in hero_list_dire:
                    hero_dire_rune_get[z.group(3)]+=1
                    rune_dire+=1
                elif z.group(3) in hero_list_rad:
                    hero_rad_rune_get[z.group(3)]+=1
                    rune_rad+=1

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

    hero_dps_pat=re.compile(r'\(\d+:\d+\)..(\w+).*?deals.(\d+).*?to.(\w+).*?')
    hero_hps_pat=re.compile(r'\(\d+:\d+\)..(\w+).*?heals.*?(\d+).*?to.(\w+).*?')
    hero_item_heal_pat=re.compile(r'\(\d+:\d+\)..(\w+).*?gets.*?(\w+).Heal')

    with open("replay_15min.txt","rb") as fin:
        for line in fin:
            l=hero_dps_pat.search(line)
            n=hero_hps_pat.search(line)
            x=hero_item_heal_pat.search(line)
            #Damage dealt to enemy heroes
            if l!=None:
                if l.group(1) in hero_list_dire and l.group(3) in hero_list_rad and 'illusion' not in line:
                    hero_dire_dict[l.group(1)]+=int(l.group(2))
                elif l.group(1) in hero_list_rad and l.group(3) in hero_list_dire and 'illusion' not in line:
                    hero_rad_dict[l.group(1)]+=int(l.group(2))
            #Healed by lifesteal,magic wand
            if n!=None:
                if n.group(3) in hero_list_dire:
                    hero_dire_heal[n.group(3)]+=int(n.group(2))
                elif n.group(3) in hero_list_rad:
                    hero_rad_heal[n.group(3)]+=int(n.group(2))
            #Healed By using flask/bottle/tango
            if x!=None:
                if x.group(1) in hero_list_dire and x.group(2)=="Tango":
                    hero_dire_tango[x.group(1)]+=1
                elif x.group(1) in hero_list_rad and x.group(2)=="Tango":
                    hero_rad_tango[x.group(1)]+=1
                elif x.group(1) in hero_list_dire and x.group(2)=="Flask":
                    hero_dire_flask[x.group(1)]+=1
                elif x.group(1) in hero_list_rad and x.group(2)=="Flask":
                    hero_rad_flask[x.group(1)]+=1
                elif x.group(1) in hero_list_dire and x.group(2)=="Bottle":
                    hero_dire_bottle[x.group(1)]+=1
                elif x.group(1) in hero_list_rad and x.group(2)=="Bottle":
                    hero_rad_bottle[x.group(1)]+=1
    fin.close()

    rad_total_hero_damage=0
    dire_total_hero_damage=0
    rad_total_heal=0
    dire_total_heal=0


    for key,val in hero_dire_dict.items():
#        key=str(key);val=str(val)
        dire_total_hero_damage+=int(val)
    for key,val in hero_rad_dict.items():
#        key=str(key);val=str(val)
        rad_total_hero_damage+=int(val)

    with open('hero_rad_skills.txt','w') as fou:
        for key,val in hero_rad_lh.items():
            key=str(key);val=str(val)
            fou.write('<'+rad_name.strip('\'\'')+'>'+'<'+player_info[key]+'>'+'<'+key+'>'+'<'+'LH/Denies/Neutrals: '+val+'/'+str(hero_rad_deny[key])+'/'+str(hero_rad_neutral[key])+'>'+'<'+'K/D/A: '+str(hero_rad_kills[key])+'/'+str(hero_rad_die[key])+str(hero_rad_assists[key])+'>'+'<'+'Damages: '+str(hero_rad_dict[key])+'>'+'<'+'Heals Received: '+str(hero_rad_heal[key]+hero_rad_tango[key]*115+hero_rad_flask[key]*400+hero_rad_bottle[key]*135)+'>'+'<'+'Smoke Participation: '+str(hero_rad_smoke_part[key])+'>'+'<'+'Ward Kills: '+str(hero_rad_ward_kill[key])+'>'+'<'+'Get Rune: '+str(hero_rad_rune_get[key])+'>'+'\n')
    fou.close()

    with open('hero_dire_skills.txt','w') as fou:
        for key,val in hero_dire_lh.items():
            key=str(key);val=str(val)
            fou.write('<'+dire_name.strip('\'\'')+'>'+'<'+player_info[key]+'>'+'<'+key+'>'+'<'+'LH/Denies/Neutrals: '+val+'/'+str(hero_dire_deny[key])+'/'+str(hero_dire_neutral[key])+'>'+'<'+'K/D/A: '+str(hero_dire_kills[key])+'/'+str(hero_dire_die[key])+'/'+str(hero_dire_assists[key])+'>'+'<'+'Damages: '+str(hero_dire_dict[key])+'>'+'<'+'Heals Received: '+str(hero_dire_heal[key]+hero_dire_tango[key]*115+hero_dire_flask[key]*400+hero_dire_bottle[key]*135)+'>'+'<'+'Smoke Participation: '+str(hero_dire_smoke_part[key])+'>'+'<'+'Ward Kills: '+str(hero_dire_ward_kill[key])+'>'+'<'+'Get Rune: '+str(hero_dire_rune_get[key])+'>'+'\n')
    fou.close()

    with open('other_info.txt','w') as fou:
        fou.write('Match: '+rad_name.strip('\'\'')+' vs. '+dire_name.strip('\'\'')+'\n')
        for item in banlist:
            fou.write('bans: '+item+'\n')
    fou.close()

    for key,val in hero_rad_heal.items():
        hero_rad_total_heal=val+hero_rad_tango[key]*115+hero_rad_flask[key]*400+hero_rad_bottle[key]*135
        rad_total_heal+=hero_rad_total_heal

    for key,val in hero_dire_heal.items():
        hero_dire_total_heal=val+hero_dire_tango[key]*115+hero_dire_flask[key]*400+hero_dire_bottle[key]*135
        dire_total_heal+=hero_dire_total_heal



    fig = pyplot.figure(figsize=(10,2))
    ratio=float(dire_total_hero_damage)/float(rad_total_hero_damage)

    ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
    ax2 = fig.add_axes([0.05, 0.3, 0.9*ratio, 0.15])

    bounds=[]
    for key in hero_rad_dict:
        bounds.append(hero_rad_dict[key])
    bounds.sort()
    for i in range(1,5):
        bounds[i]=bounds[i-1]+bounds[i]
    cmap = mpl.colors.ListedColormap(['r', 'g', 'b', 'c'])
    cmap.set_over('0.25')
    cmap.set_under('0.75')
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb1=mpl.colorbar.ColorbarBase(ax1,cmap=cmap,norm=norm,boundaries=[0]+bounds+[rad_total_hero_damage],extend='both',spacing='propotional',orientation='horizontal')
    cb1.set_label('Radiant Hero Damages Dealt')

    bounds=[]
    for key in hero_dire_dict:
        bounds.append(hero_dire_dict[key])
    bounds.sort()
    for i in range(1,5):
        bounds[i]=bounds[i-1]+bounds[i]

    norm2 = mpl.colors.BoundaryNorm(bounds,cmap.N)
    cb2=mpl.colorbar.ColorbarBase(ax2,cmap=cmap,norm=norm2,boundaries=[0]+bounds+[dire_total_hero_damage],extend='both',spacing='propotional',orientation='horizontal')
    cb2.set_label('Dire Hero Damages Dealt')
    pyplot.show()
    stat.writerow([matchid,match_duration,radiant_win_bool,hero_kills_rad,hero_kills_dire,rad_total_hero_damage,dire_total_hero_damage,rad_total_heal,dire_total_heal,first_blood_rad,count_creep_rad_kills,count_creep_dire_kills,count_creep_rad_denies,count_creep_dire_denies,smoke_counts_rad,smoke_counts_dire,glyph_rad_usage,glyph_dire_usage,count_tower_dmg_rad,count_tower_dmg_dire,neutral_kills_rad,neutral_kills_dire,ward_kills_rad,ward_kills_dire,hero_rad_index[0],hero_rad_index[1],hero_rad_index[2],hero_rad_index[3],hero_rad_index[4],hero_dire_index[0],hero_dire_index[1],hero_dire_index[2],hero_dire_index[3],hero_dire_index[4]])
#    Generate csv file for dps
#    w = csv.writer(open("hero_dps.csv", "w"))
#    for key, val in hero_rad_dict.items():
#        w.writerow([key, val])
    return dire_total_hero_damage,rad_total_hero_damage,hero_rad_dict,hero_dire_dict


def close_window():
    master.destroy()


button = Button(master, text="Exit",width=18,command=close_window)
b = Button(master, text="Compile Your Report!", width=18, command=callback)
b.pack()
button.pack()

mainloop()
