#!/usr/bin/python3
# Loadbalance script made by fish randomdata.nl

#imports
try:
    import time
    import sys
    import urllib.request, json 
    from wallbox import Wallbox
except ImportError:
   print('Error, Module wallbox and time are required, try python3 pip install wallbox time')

#parameters etc
w = Wallbox("USERNAME", "PASSWORD")
volt = 235
homeuse = 100
prevamps=16
logdata = open("logdata.txt", "a")
sleeptime = 60

import urllib.request, json

#Endlessloop with sleeptime
while True:

#Get watts info from domoticz device url
    with urllib.request.urlopen("http://192.168.88.22/json.htm?type=devices&rid=1442") as url:
        logdata.write(time.strftime("%y%m%d-%H%M%S"))
        logdata.write("-")
        data = json.loads(url.read().decode())
        watts = int(data['result'][0]['Usage'][:-4])
        print(watts,'\t watts solar')
        logdata.write(str(watts))
        logdata.write("-")
        amps = round(((watts-homeuse)/volt))
        print(watts-homeuse,'\t minus homeuse')
        print(amps,'\t Amps setting wallbox')
        logdata.write(str(amps))
        logdata.write("\n")

    # Authenticate with the wallbox api credentials above
    w.authenticate()

    # Print a list of chargers in the account
    print(w.getChargersList())

    # Get charger data for all chargers in the list, then change amps on chargers

    if amps < 6:
        amps = 6

    if amps != prevamps:
        for chargerId in w.getChargersList():
            print('Setting from ',prevamps,' A to ',amps,' A') 
            chargerStatus = w.getChargerStatus(chargerId)
            w.setMaxChargingCurrent(chargerId, amps)
            chargerStatus = w.getChargerStatus(chargerId)
            prevamps = amps

    #Closing part (logs etc)
    #logdata.close()

    print("SLEEP start "+time.strftime('%H:%M:%S %Z %d-%m-%Y'))
    time.sleep(sleeptime)
