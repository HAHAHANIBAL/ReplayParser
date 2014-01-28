#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import os
import re

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
