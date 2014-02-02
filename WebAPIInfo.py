#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib2
import re
import logging

class matchinfo:
    rad_win_bool=1
    dire_team=''
    rad_team=''
    cluster_info=0
    duration=0
    account_id=[]
    hero_id=[]
    player_name=[]
    ban_id=[]
    hero_names=[]
    hero_bans_names=[]
    player_dict={}

#testing purpose
#matchid=475880380

def getmatch(matchid):
    #My API key
    APIkey='AFD368B9F9928B7F3C732CED8B599DA1'
    #Import matchid here
    userMainUrl='https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='+str(matchid)+'&key='+APIkey
    req=urllib2.Request(userMainUrl)

    try:
        resp=urllib2.urlopen(req)
    except Exception as ex:
        logging.info('failed to get match id: %d', matchid)

    respHtml=resp.read()
    rad_win_pat=re.compile(r'"radiant_win":.(\w+)')
    #rad_user_info=re,compile(r'')
    #dire_user_info=re.compile(r'')
    cluster_info_pat=re.compile(r'"cluster":.(\d+)')
    dire_team_pat=re.compile(r'"dire_name":.\"(.*?)\"')
    rad_team_pat=re.compile(r'"radiant_name":.\"(.*?)\"')
    duration_pat=re.compile(r'"duration":.(\d+)')
    account_pat=re.compile(r'"account_id":.(\d+)')
    hero_pat=re.compile(r'"hero_id":.(\d+)')


    if 'false' in rad_win_pat.findall(respHtml):
        matchinfo.rad_win_bool=0
    else:
        matchinfo.rad_win_bool=1

    #convert the lists generated to int or strings
    matchinfo.dire_team=str(dire_team_pat.findall(respHtml)).strip('[]')
    matchinfo.rad_team=str(rad_team_pat.findall(respHtml)).strip('[]')
    matchinfo.cluster_info=int((str(cluster_info_pat.findall(respHtml)).strip('[]')).strip('\'\''))
    matchinfo.duration=int(str(duration_pat.findall(respHtml)).strip('[]').strip('\'\''))
    matchinfo.account_id=account_pat.findall(respHtml)
    matchinfo.hero_id=hero_pat.findall(respHtml)[0:10]
    matchinfo.player_name=getuserName_Hero(matchinfo.account_id)

    hero_id_all=hero_pat.findall(respHtml)
    #Construct Ban Hero list
    for item in hero_id_all:
        if item not in matchinfo.hero_id:
            matchinfo.ban_id.append(item)
    #Compile the heroes id into names
    for item in matchinfo.hero_id:
        fin=open('hero_index.txt','r')
        for line in fin:
            if re.compile(r'(\w+).*,(\d+)').search(line).group(2)==item:
                matchinfo.hero_names.append(re.compile(r'(\w+).*,(\d+)').search(line).group(1))
        fin.close()
    #Compile the ban list into names
    for item in matchinfo.ban_id:
        fin=open('hero_index.txt','r')
        for line in fin:
            if re.compile(r'(\w+).*,(\d+)').search(line).group(2)==item:
                matchinfo.hero_bans_names.append(re.compile(r'(\w+).*,(\d+)').search(line).group(1))
        fin.close()

    #Final step, combine all data player info and their heroes together
    for i in range(0,10):
        matchinfo.player_dict[matchinfo.hero_names[i]]=matchinfo.player_name[i]


    return matchinfo

def getuserName_Hero(account_id):
    for item in account_id:
        dotabuffurl='http://dotabuff.com/players/'+item
        req=urllib2.Request(dotabuffurl)
        try:
            resp=urllib2.urlopen(req)
        except Exception as ex:
            logging.info('failed to get account id: %d', item)
        respHtml=resp.read()
        player_pat=re.compile('<span class="symbol verified" rel="tooltip".title=\"This.player.*?as.(.*?).\">')
        player_name=(str(player_pat.findall(respHtml)).strip('[]')).strip('\'\'')
        matchinfo.player_name.append(player_name)
    return matchinfo.player_name

#testing purpose

#print matchinfo.player_dict
#print matchinfo.hero_bans_names


