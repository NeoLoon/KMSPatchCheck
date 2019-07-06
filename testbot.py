### Copyright (c) 2018 - 2019 Neo
### MIT License
### Version 1.0.8 beta release

import os
import platform
import subprocess
import discord
import urllib.request
import asyncio
from hashlib import md5

TOKEN = '###DISCORD TOKEN###'

client = discord.Client()
oldhash = 0
newhash = 0
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
async def kmscheck(down):
    global oldhash, newhash, newver, oldver
    urlsd = "http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/00{}to00{}.patch".format(newver, oldver, newver)
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
            print("You are getting this error because you are using 0.16.x version of async, please update to V.1.0+ to use this bot")
            os._exit(1)

        except Exception as e:
            print(e)
            os._exit(1)

@client.event
async def kmsMcheck(down):
    c = 0
    global oldhash, newhash, newver, oldver, minorsize
    urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/ExePatch.dat'.format(oldver)
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
                print("You are getting this error because you are using 0.16.x version of async, please update to V.1.0+ to use this bot")
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
    global oldhash, newhash, newverT, oldverT
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

            return 9
        except(urllib.error.HTTPError):
            print("File doesn't exist")
            await asyncio.sleep(60)

        except(AtrributeError):
            print("You are getting this error because you are using 0.16.x version of async, please update to V.1.0+ to use this bot")
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
            print("You are getting this error because you are using 0.16.x version of async, please update to V.1.0+ to use this bot")
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
async def ServerStatus():
    # if they are down -> update check, sleep timer, etc. will come in the future
    syscheck = platform.system()
    # needs to find a Test-NetConnection replacement for python3
    if syscheck != "Windows":
        print("This feature is only avaliable to Windows Platform as of now")
        return 1
    m = "TcpTestSucceeded : True"
    live = subprocess.getoutput(["powershell.exe", "Test-NetConnection INSERTIP -port INSERTPORT"])
    if m in live:
        msg = "UP"
    else:
        msg = "DOWN"
    # test server needs different logic as patch files are up first (prob needs different function)
    test = subprocess.getoutput(["powershell.exe", "Test-NetConnection INSERTIP -port INSERTPORT"])
    if m in test:
        msg1 = "UP"
    else:
        msg1 = "DOWN"
    try:
        await client.get_channel(###Channel ID###).send(msg)
        await client.get_channel(###Channel ID###).send(msg1)
    except Exception as e:
        print(e)
    return 0

@client.event
async def on_ready():
    a = 0
    enable = 0 #Patch download
    while 1:
        a = int(input("\nChoose from these:\n1. KMS check\n2. KMS minor check\n3. KMST check\n4. JMS check\n5. Enable Patch Download\n6. Quit\n7. Server Check(BETA)\n\nChoice? : "))
        try:
            if a == 1:
                await kmscheck(enable)
            elif a == 2:
                await kmsMcheck(enable)
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
                os._exit(0)
            elif a == 7:
                await ServerStatus()
            await updateVer()
        except:
            os._exit(0)

client.run(TOKEN)
