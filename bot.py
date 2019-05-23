### Copyright (c) 2018 - 2019 Neo
### MIT License
### Version 1.0.3 stable release

import os
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
            await client.get_channel(###Channel ID ###).send(msg)
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
            open('ver.txt', 'w').close()
            newver+=1
            oldver+=1
            x = open("ver.txt", "w")
            x.write(str(newver) + "\n")
            print("Waiting for 5 min...")
            await asyncio.sleep(300) #wait 5 min and write the ExePatch.dat size
            urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/ExePatch.dat'.format(oldver)
            check = urllib.request.urlopen(urls)
            mdata = int(check.info()['Content-Length']) #get metadata
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
            x.write(str(size) + "\n")
            print("Write Complete, Killing bot")
            x.close()
            return 0
        except:
            await asyncio.sleep(60)

@client.event
async def kmsMcheck(down):
    c = 0
    global oldhash, newhash, newver, oldver
    urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/Version.info'.format(oldver)
    print(urls)
    print("Start checking for KMS minor patch...")
    while 1:
        urllib.request.urlretrieve(urls, filename='Version.info')
        if c == 0:
            f=open("Version.info","rb")
            data=f.read()
            f.close()
            oldhash = md5(data).hexdigest()
            c += 1
        f=open("Version.info","rb")
        data=f.read()
        f.close()
        newhash = md5(data).hexdigest()
        if oldhash != newhash:
            print("Patch found!")
            f = open("verM.txt", "r")
            ver = int(f.readline()) #Read the version to compare to the
            minor = int(f.readline())
            f.close()
            if ver != oldver:
                ver = oldver
                minor = 2
            urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/ExePatch.dat'.format(ver)
            check = urllib.request.urlopen(urls)
            mdata = int(check.info()['Content-Length']) #get metadata
            datemod = check.info()['Last-Modified']
            size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
            msg = "@everyone KMS ver 1.2.{}({}) Minor Patch is up!\n\nPatch Size is: {}MB\nLast MapleStory.exe size was: {}MB\n\nDate uploaded: {}".format(ver, minor, size, prevsize, datemod)
            open('ver.txt', 'w').close()
            x = open("ver.txt", "w")
            x.write(str(newver) + "\n" + str(size) + "\n")
            x.close()
            open('verM.txt', 'w').close()
            x = open("verM.txt", "w")
            x.write(str(ver) + "\n" + str(minor+1) + "\n")
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
            await client.get_channel(###Channel ID ###).send(msg)
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
            await client.get_channel(###Channel ID ###).send(msg)
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
            open('verT.txt', 'w').close()
            x = open("verT.txt", "w")
            x.write(str(newverT))
            x.close()
            return 0
        except:
            await asyncio.sleep(60)

@client.event
async def jmscheck(down):
    f = open("verJMS.txt", "r")
    newver = int(f.readline())
    print("Detected version: {}".format(newver))
    f.close()
    oldver = newver - 1
    urlsd = "http://webdown2.nexon.co.jp/maple/patch/patchdir/00{}/00{}to00{}.patch".format(newver, oldver, newver)
    print(urls)
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
            await client.get_channel(###Channel ID ###).send(msg)
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
            open('verJMS.txt', 'w').close()
            newver+=1
            oldver+=1
            x = open("verJMS.txt", "w")
            x.write(str(newver) + "\n")
            print("Write Complete, Killing bot")
            x.close()
            return 0
        except:
            await asyncio.sleep(120)

@client.event
async def on_ready():
    a = 0
    enable = 0 #Patch download
    while 1:
        a = int(input("\nChoose from these:\n1. KMS check\n2. KMS minor check\n3. KMST check\n4. JMS check\n5. Enable Patch Download\n6. Quit\n\nChoice? : "))
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
                exit()
        except:
            exit()

client.run(TOKEN)
