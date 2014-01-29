#!/usr/bin/python
#-*- coding: utf-8 -*-
import re


hero_index=re.compile(r',.?(.*?),.(\d+)')
fou=open('hero_index.txt','w')

with open('heroes.txt','rb') as fin:
    for line in fin:
        fou.write(str(hero_index.search(line).group(1))+','+str(hero_index.search(line).group(2))+'\n')

fou.close()