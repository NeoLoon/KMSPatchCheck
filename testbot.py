### Copyright (c) 2018 - 2019 Neo
### MIT License
### Version 1.0.9 beta release

import os
import socket
import discord
import urllib.request
import asyncio
try:
    ze = 1 #zeep check
    import zeep
    import pytz
    import datetime
except:
    ze = 0 #doesn't exist
    print("Either zeep, pytz or datetime is not installed, KMS check will run with a traditional method.")

TOKEN = '###DISCORD TOKEN###'

client = discord.Client()
patchvoid = 0

f = open("ver.txt", "r")
newver = int(f.readline())
prevsize = float(f.readline())
minorsize = float(f.readline())
f.close()
oldver = newver - 1

f = open("verT.txt", "r")
newverT = int(f.read())
f.close()
oldverT = newverT - 1

print("Version check \nOld: ", oldver , "\nNew: ", newver,"\n\nOld KMST: ", oldverT, "\nNew KMST: ", newverT)

@client.event
async def timecheck():
    client = zeep.Client('http://api.maplestory.nexon.com/soap/maplestory.asmx?WSDL') #Get WSDL
    maintime = client.service.GetInspectionInfo()._value_1._value_1[0]["InspectionInfo"].startDateTime #Get Time from patch
    patch_m = int(maintime.strftime("%m")) #Get Month
    patch_d = int(maintime.strftime("%d")) #Get day
    patch_h = int(maintime.strftime("%H")) #Get hour
    print('{} {} {}'.format(patch_m, patch_d, patch_h)) #Print for beta

    kst = pytz.timezone('Asia/Seoul') #set timezone
    kst_time = datetime.datetime.now(tz=kst)
    month = int(kst_time.strftime("%m")) #get current month
    day = int(kst_time.strftime("%d")) #get current day
    hour = int(kst_time.strftime("%H")) #get current hour
    print('{} {} {}'.format(month, day, hour)) #Print for beta

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
        elif (day < patch_d) & ((hour - patch_h) > 0):
            print("Day is different")
            await asyncio.sleep(86400)
            await timecheck()
        elif hour < patch_h:
            print("You still have 1+ hour until patch")
            h = patch_h - hour
            await asynic.sleep(3600*(h-1))
            return 0
    except Exception as e:
        print(e)

    print("You already passed the date that was provided by API, skipping")
    return 0 #server is up

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

            newver+=1
            oldver+=1
            print("Waiting for 5 min...")
            await asyncio.sleep(300) #wait 5 min and write the ExePatch.dat size

            x = open("verM.txt", "w")
            x.write(str(2) + "\n")
            x.close()

            x = open("ver.txt", "w")
            x.write(str(newver) + "\n")

            urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/ExePatch.dat'.format(oldver)
            check = urllib.request.urlopen(urls)
            mdata = int(check.info()['Content-Length']) #get metadata
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB

            x.write(str(size) + "\n")
            x.write(str(mdata) + "\n")
            print("Write Complete, Killing bot")
            x.close()

            return 0
        except(urllib.error.HTTPError):
            print("File doesn't exist")
            await asyncio.sleep(50)

        except(AtrributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
            os._exit(1)

        except Exception as e:
            print(e)
            os._exit(1)

@client.event
async def kmsMcheck(down, check):
    global newver, oldver, minorsize
    urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/ExePatch.dat'.format(oldver)
    if check == 0:
        await ServerStatus(1)
    print("Start checking for KMS minor patch...")
    while 1:
        check = urllib.request.urlopen(urls)
        mdata = int(check.info()['Content-Length'])
        if mdata != minorsize:
            print("Patch found!")

            f = open("verM.txt", "r")
            minor = int(f.readline())
            f.close()

            datemod = check.info()['Last-Modified']
            size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
            msg = "@everyone KMS ver 1.2.{}({}) Minor Patch is up!\n\nPatch Size is: {}MB\nLast MapleStory.exe size was: {}MB\n\nDate uploaded: {}".format(oldver, minor, size, prevsize, datemod)
            try:
                await client.get_channel(###Channel ID###).send(msg)
            except(AttirbuteError):
                print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
                os._exit(1)

            x = open("ver.txt", "w")
            x.write(str(oldver) + "\n" + str(size) + "\n" + str(mdata) +"\n")
            x.close()

            x = open("verM.txt", "w")
            x.write(str(minor+1) + "\n")
            x.close()

            if down == 1:
                if os.path.isdir("./KMSM") == False:
                    try:
                        os.mkdir("./KMSM")
                    except OSError:
                        print("Failed to create directory.")
                        break
                    else:
                        print("Directory KMSM has been created")
                filename = "./KMSM/ExePatch.dat"
                print("Downloading...")
                urllib.request.urlretrieve(urls, filename)
                print("Download Complete. (saved to ./KMSM folder)")
            print("Write Complete, Killing bot")
            return 0
        await asyncio.sleep(120)

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
            newverT+=1
            oldverT+=1

            x = open("verT.txt", "w")
            x.write(str(newverT))
            x.close()

            print("Checking for server...")
            await ServerStatus(2)

            return 0
        except(urllib.error.HTTPError):
            print("File doesn't exist")
            await asyncio.sleep(60)

        except(AtrributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
            os._exit(1)

        except Exception as e:
            print(e)
            os._exit(1)

@client.event
async def jmscheck(down):
    f = open("verJMS.txt", "r")
    newver = int(f.readline())
    print("Detected version: {}".format(newver))
    f.close()

    oldver = newver - 1
    urlsd = "http://webdown2.nexon.co.jp/maple/patch/patchdir/00{}/00{}to00{}.patch".format(newver, oldver, newver)
    print(urlsd)
    print("Start checking for JMS patch...")
    while 1:
        try:
            urllib.request.urlopen(urlsd)
            print("Patch found!")
            check = urllib.request.urlopen(urlsd)
            mdata = int(check.info()['Content-Length']) #get metadata
            datemod = check.info()['Last-Modified']

            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
                msg = "@everyone JMS ver.{} Patch is up!\n\nPatch Size is: {}GB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
                msg = "@everyone JMS ver.{} Patch is up!\n\nPatch Size is: {}MB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            await client.get_channel(###Channel ID###).send(msg)

            if down == 1:
                if os.path.isdir("./JMS") == False:
                    try:
                        os.mkdir("./JMS")
                    except OSError:
                        print("Failed to create directory.")
                        break
                    else:
                        print("Directory JMS has been created")
                filename = "./JMS/00{}to00{}.patch".format(oldver, newver)
                print("Downloading...")
                urllib.request.urlretrieve(urlsd, filename)
                print("Download Complete. (saved to ./JMS folder)")

            newver+=1
            oldver+=1
            x = open("verJMS.txt", "w")
            x.write(str(newver) + "\n")
            print("Write Complete, Killing bot")
            x.close()

            return 0
        except(urllib.error.HTTPError):
            print("File doesn't exist")
            await asyncio.sleep(120)

        except(AtrributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
            os._exit(1)

        except Exception as e:
            print(e)
            os._exit(1)

@client.event
async def updateVer():
    global newver, prevsize, minorsize, oldver, newverT, oldverT
    f = open("ver.txt", "r")
    newver = int(f.readline())
    prevsize = float(f.readline())
    minorsize = float(f.readline())
    f.close()
    oldver = newver - 1

    f = open("verT.txt", "r")
    newverT = int(f.read())
    f.close()
    oldverT = newverT - 1
    return 0

@client.event
async def ServerStatus(x):
    # 1 stands for live and 2 stands for test
    a = 0
    if x == 1:
        ip = 'IP ADDRESS' #Live Server IP
    elif x == 2:
        ip = 'IP ADDRESS' #Test Server IP
    port = PORT #Server Port

    try:
        while 1:
            print("check {}".format(a))
            a += 1
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
                    except(AttirbuteError):
                        print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
                    except Exception as e:
                        print(e)
                    break #End the ping loop and return
            await asyncio.sleep(30)
    except Exception as e:
        ping.close()
        msg = "live server is down, starting patch check"
        try:
            await client.get_channel(###Channel ID###).send(msg)
            return 0
        except(AttirbuteError):
            print("You are getting this error because you are using 0.16.x version of async, please update it to V.1.0+ to use this bot")
        except Exception as e:
            print(e)
        return 0
    return 0

@client.event
async def on_ready():
    a = 0
    check = 0 #ServerStatus
    enable = 0 #Patch download
    while 1:
        a = int(input("\nChoose from these:\n1. KMS check\n2. KMS minor check\n3. KMST check\n4. JMS check\n5. Enable/Disable Patch Download\n6. Skip Server Status check for KMS\n7. Quit\n8. Enable/Disable SOAP time check\n\nChoice? : "))
        try:
            if a == 1:
                if ze == 1:
                    await timecheck()
                print("return check")
                await kmscheck(enable, check)
            elif a == 2:
                await kmsMcheck(enable, check)
            elif a == 3:
                await KMSTcheck(enable)
            elif a == 4:
                await jmscheck(enable)
            elif a == 5:
                if enable == 0:
                    enable = 1;
                    print("Patch download has been enabled")
                else:
                    enable = 0;
                    print("Patch download has been disabled")
            elif a == 6:
                if check == 0:
                    check = 1;
                    print("OK, server status check will be skipped")
                else:
                    check = 0;
                    print("OK, server status will be checked")
            elif a == 7:
                os._exit(0)
            elif a == 8:
                if ze == 1:
                    ze = 0
                    print("SOAP check has been disabled")
                else:
                    ze = 0
                    print("SOAP check has been enabled")
            await updateVer()
        except:
            os._exit(0)

client.run(TOKEN)
