# oneDayTrip.py
#
# Find all instances of baseball teams that played a one-day road trip,
#  defined as any 3-day period where a team played
#   at least one home game on day 1,
#   at least one road game on day 2,
#   and at least one home game on day 3.
#
# Input: Download the Game Logs from www.retrosheet.org (no need to unzip)

import datetime, glob, re, sys, zipfile
from collections import defaultdict

## import os
## os.chdir(r'where_the_gamelogs_are') # if not in the same directory as this program

def default_itinerary():
    return [ord('0') for x in range(366)]

itinerary = defaultdict(default_itinerary)
tripsFound = 0

def blab(what):
    print(datetime.datetime.now().strftime("%H:%M:%S"), what, file=sys.stderr)

def convertDate(sd):
    y, m, d = int(sd[:4]), int(sd[4:6]), int(sd[-2:])
    return datetime.date(y, m, d).toordinal() - datetime.date(y, 1, 1).toordinal()

def oneGame(gameline):
    fields = gameline.split(',',7)
    if len(fields) < 7:
        return
    yyyymmdd = fields[0].strip('"')[-8:]
    vt = fields[3].strip('"')
    ht = fields[6].strip('"')
    yr = yyyymmdd[:4]
    dayOfYear = convertDate(yyyymmdd)
    
    itinerary[yr + vt][dayOfYear] |= 2
    itinerary[yr + ht][dayOfYear] |= 1
    
blab("Start oneDayTrip.py")    

for glArch in glob.glob('gl*.zip'):
    zipArch = zipfile.ZipFile(glArch,'r')
    for gamelogfile in zipArch.namelist():
        for g in str(zipArch.read(gamelogfile)).split(r'\n'):
            oneGame(g)

for yearTeam in sorted(itinerary.keys()):
    strItin = ''.join([chr(x) for x in itinerary[yearTeam] ])
    for matched in re.finditer(r'(?=[13][23][13])', strItin):
        tripsFound += 1
        year, team = yearTeam[:4], yearTeam[-3:]
        roadDate = datetime.date(int(year),1,1) + datetime.timedelta(days=matched.start()+1)
        print("%s %s http://www.retrosheet.org/boxesetc/%s/V%s0%s.htm"
              % (team, roadDate.strftime("%m/%d"), year, team, year))

blab("Found %d trips" % (tripsFound))



    
