### Copyright (c) 2018 - 2019 Neo
### MIT License
### Version 1.0.13-2 stable release

import os
import socket
import discord
import urllib.request
import asyncio
import fileinput
try:
    ze = 1 #zeep check
    import zeep
    import pytz
    import datetime
except:
    ze = 0 #doesn't exist
    print("Either zeep, pytz or datetime is not installed, KMS check will run with a traditional method.")

TOKEN = '###DISCORD ID###'

client = discord.Client()
kms_choice = 0

f = open("ver.txt", "r")
newver = int(f.readline())
newverT = int(f.readline())
patch_string = f.readline().strip()
f.close()
oldver = newver - 1
oldverT = newverT - 1

print("Version check:\n\nKMS version:", newver,"\nKMST version:", newverT)

@client.event
async def timecheck():
    global kms_choice, minorver, patch_string
    client_zeep = zeep.Client('http://api.maplestory.nexon.com/soap/maplestory.asmx?WSDL') #Get WSDL
    info = client_zeep.service.GetInspectionInfo()._value_1._value_1[0]["InspectionInfo"]
    maintime = info.startDateTime #Get Time from patch
    maintime_end = info.endDateTime #Get Time from patch
    detail = info.strObstacleContents #Get the name of the patch
    patch_i = ""

    #GET PATCH INFO
    if ("긴급점검") in detail:
        print("Emergency Maintenance")
        patch_i = "Emergency Maintenance Schedule"
    elif ("임시점검") in detail:
        print("Unscheduled Maintenance")
        patch_i = "Unscheduled Maintenance Schedule"
    elif ("점검") in detail:
        print("Not a patch, maintenance.")
        patch_i = "New Maintenance Schedule"
    elif ("마이너") in detail:
        print("Minor patch will be checked")
        patch_i = "New Minor Patch Schedule"
    elif ("클라이언트 패치") in detail:
        print("Client patch will be checked")
        patch_i = "New Patch Schedule"
        kms_choice = 1
    else:
        print(detail)
        print("Unable to get the patch info, you can report this to https://github.com/NeoLoon/KMSPatchCheck/issues")
        print("If this issue persists please skip this by using Option 7")

    patch_m = int(maintime.strftime("%m")) #Get patch month
    patch_d = int(maintime.strftime("%d")) #Get patch day
    patch_h = int(maintime.strftime("%H")) #Get patch hour
    patch_min = int(maintime.strftime("%M")) #Get current min
    end_patch_d = int(maintime_end.strftime("%d")) #Patch end date
    end_patch_h = int(maintime_end.strftime("%H")) #Patch ending hour
    end_patch_min = int(maintime_end.strftime("%M")) #Patch ending min

    kst = pytz.timezone('Asia/Seoul') #set timezone
    kst_time = datetime.datetime.now(tz=kst)
    month = int(kst_time.strftime("%m")) #get current month
    day = int(kst_time.strftime("%d")) #get current day
    hour = int(kst_time.strftime("%H")) #get current hour
    min = int(kst_time.strftime("%M")) #get current min

    if patch_string != detail:
        msg = ("{}\n\n{}\nPatch/Maintenance is expected to start at {}:{} KST.\nPatch/Maintenance will be done around {}:{} KST.".format(patch_i, detail, patch_h, patch_min, end_patch_d, end_patch_min)) #Will think of better msg next time
        for line in fileinput.input('ver.txt', inplace=True):
            print(line.rstrip().replace(str(patch_string), str(detail)))
        fileinput.close()
        try:
            await client.get_channel(###Channel ID###).send(msg)
        except Exception as e:
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
            os._exit(1)

    sleep = 0
    try:
        if month < patch_m:
            print("Month is different")
            if month == 2:
                sleep = ((28 - day) + patch_d - 1) * 86400
            else:
                sleep = ((30 - day) + patch_d - 1) * 86400 #31 and 30 fix is coming later
            await asyncio.sleep(sleep)
            await timecheck()
        elif ((patch_d - day) > 1) or ((patch_d - day) > 0) and ((patch_h - hour) > 0) and (kms_choice == 0):
            print("Day is different, waiting for a day")
            await asyncio.sleep(86400)
            await timecheck()
        elif (hour < patch_h) or (day < patch_d):
            if (patch_h - hour) < 0:
                h = 24 - hour + patch_h
            else:
                h = patch_h - hour
            print("You still have {} hour(s) until patch/maintenance".format(h))
            await asyncio.sleep(3600*(h-1) + ((60 - min) * 60))
            if kms_choice == 1:
                return 0
            else:
                await asyncio.sleep(3600)
                await timecheck()
        elif hour == patch_h:
            printf("Patch has started")
            if kms_choice == 1:
                return 0
            else:
                await asyncio.sleep(3600)
                await timecheck()
        else:
            print("You either already passed the date that was given by API or the game is having a maintenance, sleeping for 1 hour for new info")
            await asyncio.sleep(3600) #need more information to handle this
            await timecheck()
    except Exception as e:
        print(e)

    return 0

@client.event
async def kmscheck(down, check):
    global newver, oldver
    urlsd = "http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/00{}to00{}.patch".format(newver, oldver, newver)
    if check == 0:
        await ServerStatus(1)
    print(urlsd)
    print("Start checking for KMS patch...")
    while 1:
        try:
            urllib.request.urlopen(urlsd)
            print("Patch found!")
            check = urllib.request.urlopen(urlsd)
            mdata = int(check.info()['Content-Length']) #get metadata
            datemod = check.info()['Last-Modified']
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
                msg = "@everyone KMS ver 1.2.{} Patch is up!\n\nPatch Size is: {}GB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
                msg = "@everyone KMS ver 1.2.{} Patch is up!\n\nPatch Size is: {}MB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            await client.get_channel(###Channel ID###).send(msg)

            if down == 1:
                if os.path.isdir("./KMS") == False:
                    try:
                        os.mkdir("./KMS")
                    except OSError:
                        print("Failed to create directory.")
                        break
                    else:
                        print("Directory KMS has been created")
                filename = "./KMS/00{}to00{}.patch".format(oldver, newver)
                print("Downloading...")
                urllib.request.urlretrieve(urlsd, filename)
                print("Download Complete. (saved to ./KMS folder)")

            for line in fileinput.input('ver.txt', inplace=True):
                print(line.rstrip().replace(str(newver), str(newver+1)))
            fileinput.close()

            print("Write Complete, Killing bot")
            return 0
        except(urllib.error.HTTPError):
            print("File doesn't exist")
            await asyncio.sleep(50)

        except(AttributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
            os._exit(1)

        except Exception as e:
            print(e)
            os._exit(1)

@client.event
async def KMSTcheck(down):
    global newverT, oldverT
    urls = "http://maplestory.dn.nexoncdn.co.kr/PatchT/0{}/0{}to0{}.patch".format(newverT, oldverT, newverT)
    print(urls)
    print("Start checking for KMST patch...")
    while 1:
        try:
            urllib.request.urlopen(urls)
            print("Patch found!")
            check = urllib.request.urlopen(urls)
            mdata = int(check.info()['Content-Length']) #get metadata

            datemod = check.info()['Last-Modified']
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
                msg = "@everyone KMST ver 1.2.0{} Patch is up!\n\nPatch Size is: {}GB\nDate uploaded: {}\nLink: {}".format(int(newverT-1000),size, datemod, urls)
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
                msg = "@everyone KMST ver 1.2.0{} Patch is up!\n\nPatch Size is: {}MB\nDate uploaded: {}\nLink: {}".format(int(newverT-1000),size, datemod, urls)
            await client.get_channel(###Channel ID###).send(msg)

            if down == 1:
                if os.path.isdir("./KMST") == False:
                    try:
                        os.mkdir("./KMST")
                    except OSError:
                        print("Failed to create directory.")
                        break
                    else:
                        print("Directory KMST has been created")
                filename = "./KMST/00{}to00{}.patch".format(oldverT, newverT)
                print("Downloading...")
                urllib.request.urlretrieve(urls, filename)
                print("Download Complete. (saved to ./KMST folder)")

            for line in fileinput.input('ver.txt', inplace=True):
                print(line.rstrip().replace(str(newverT), str(newverT+1)))
            fileinput.close()

            print("Checking for server...")
            await ServerStatus(2)

            return 0
        except(urllib.error.HTTPError):
            print("File doesn't exist")
            await asyncio.sleep(60)

        except(AttributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
            os._exit(1)

        except Exception as e:
            print(e)
            os._exit(1)

@client.event
async def updateVer():
    global newver, oldver, newverT, oldverT, patch_string
    f = open("ver.txt", "r")
    newver = int(f.readline())
    newverT = int(f.readline())
    patch_string = f.readline().strip()
    f.close()

    oldver = newver - 1
    oldverT = newverT - 1
    return 0

@client.event
async def ServerStatus(x):
    # DOES NOT WORK FOR GLOBAL SERVER
    # 1 stands for live and 2 stands for test
    if x == 1:
        ip = 'IP ADDRESS' #Live Server IP
    elif x == 2:
        ip = 'IP ADDRESS' #Test Server IP
    if ('IP ADDRESS') in ip:
        print("Please fix your IP address in script")
        return 0
    port = PORT #Server Port

    try:
        print("Checking if the server is alive...")
        while 1:
            ping = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ping.settimeout(15) #timeout is manually set to 15 sec.
            try:
                ping.connect((ip, port))
                msg = b'ping'
                ping.send(msg)
                data = ping.recv(1024)
                ping.close()
            except Exception as e:
                if x == 1:
                    raise Exception
                else:
                    data = ''
                    ping.close()

            if data: #Check if packet is empty
                if x != 1:
                    msg = "Test server is up"
                    try:
                        await client.get_channel(###Channel ID###).send(msg)
                        return 0
                    except(AttributeError):
                        print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
                    except Exception as e:
                        print(e)
                    break #End the ping loop and return
            await asyncio.sleep(30)
    except Exception as e:
        ping.close()
        msg = "Live server is down, starting patch check"
        try:
            await client.get_channel(###Channel ID###).send(msg)
            return 0
        except(AttributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
        except Exception as e:
            print(e)
        return 0
    return 0

@client.event
async def on_ready():
    global kms_choice, ze
    a = 0
    check = 0 #ServerStatus
    enable = 0 #Patch download
    while 1:
        a = int(input("\nChoose from these:\n1. KMS check\n2. KMST check\n3. Enable/Disable Patch Download\n4. Skip Server Status check for KMS\n5. Enable/Disable SOAP time check\n6. Quit\n\nChoice? : "))
        try:
            if a == 1:
                if ze == 1:
                    while kms_choice == 0:
                        await timecheck()
                    check = 1
                await kmscheck(enable, check)
            elif a == 2:
                await KMSTcheck(enable)
            elif a == 3:
                if enable == 0:
                    enable = 1;
                    print("Patch download has been enabled")
                else:
                    enable = 0;
                    print("Patch download has been disabled")
            elif a == 4:
                if check == 0:
                    check = 1;
                    print("OK, server status check will be skipped")
                else:
                    check = 0;
                    print("OK, server status will be checked")
            elif a == 5:
                if ze == 1:
                    ze = 0
                    print("SOAP check has been disabled")
                else:
                    ze = 0
                    print("SOAP check has been enabled")
            elif a == 6:
                os._exit(0)
            await updateVer()
        except Exception as e:
            print(e)
            os._exit(0)

client.run(TOKEN)
