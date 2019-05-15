### Copyright (c) 2018 ~ 2019 Neo
### MIT License
### Version 1.0.1 release

import discord
import urllib.request
import asyncio
from hashlib import md5

TOKEN = '###DISCORD TOKEN###'

client = discord.Client()
e = 0
c = 0
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
    global e, c, oldhash, newhash, newver, oldver
    while 1:
        urlsd = "http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/00{}to00{}.patch".format(newver, oldver, newver)
        print(urlsd)
        try:
            urllib.request.urlopen(urlsd)
            check = urllib.request.urlopen(urlsd)
            mdata = int(check.info()['Content-Length']) #get metadata
            datemod = check.info()['Last-Modified']
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
                msg = "@everyone KMS ver 1.2.{} Patch is up!\n\nPatch Size is: {}GB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
                msg = "@everyone KMS ver 1.2.{} Patch is up!\n\nPatch Size is: {}MB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            newver+=1
            await client.get_channel(###Channel ID ###).send(msg)
            if down == 1:
                filename = "00{}to00{}.patch".format(oldver, newver)
                print("Downloading...")
                urllib.request.urlretrieve(urlsd, filename)
                print("Download Complete.")
            await asyncio.sleep(10)
            open('ver.txt', 'w').close()
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
            await asyncio.sleep(50)

@client.event
async def kmsMcheck(down):
    global e, c, oldhash, newhash, newver, oldver
    urls = 'http://maplestory.dn.nexoncdn.co.kr/Patch/00{}/Version.info'.format(oldver)
    print("hello")
    while 1:
        urllib.request.urlretrieve(urls, filename='Version.info')
        if c == 0:
            f=open("Version.info","rb")
            data=f.read()
            f.close()
            oldhash = md5(data).hexdigest()
            c += 1
        urllib.request.urlretrieve(urls, filename='Version.info')
        f=open("Version.info","rb")
        data=f.read()
        f.close()
        newhash = 1 #md5(data).hexdigest()
        if oldhash != newhash:
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
                filename = "ExePatch.dat".format(oldver, newver)
                print("Downloading...")
                urllib.request.urlretrieve(urls, filename)
                print("Download Complete.")
            print("Write Complete, Killing bot")
            await client.get_channel(###Channel ID ###).send(msg)
            return 0
        await asyncio.sleep(120)

@client.event
async def KMSTcheck(down):
    global e, c, oldhash, newhash, newverT, oldverT
    while 1:
        urls = "http://maplestory.dn.nexoncdn.co.kr/PatchT/0{}/0{}to0{}.patch".format(newverT, oldverT, newverT)
        print(urls)
        try:
            urllib.request.urlopen(urls)
            check = urllib.request.urlopen(urls)
            mdata = int(check.info()['Content-Length']) #get metadata
            datemod = check.info()['Last-Modified']
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
                msg = "@everyone KMST ver 1.2.0{} Patch is up!\n\nPatch Size is: {}GB\nDate uploaded: {}\nLink: {}".format(int(newverT-1000),size, datemod, urls)
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
                msg = "@everyone KMST ver 1.2.0{} Patch is up!\n\nPatch Size is: {}MB\nDate uploaded: {}\nLink: {}".format(int(newverT-1000),size, datemod, urls)
            newverT+=1
            await client.get_channel(###Channel ID ###).send(msg)
            oldverT+=1
            if down == 1:
                filename = "00{}to00{}.patch".format(oldver, newver)
                print("Downloading...")
                urllib.request.urlretrieve(urls, filename)
                print("Download Complete.")
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
    f.close()
    oldver = newver - 1
    while 1:
        urlsd = "http://webdown2.nexon.co.jp/maple/patch/patchdir/00{}/00{}to00{}.patch".format(newver, oldver, newver)
        print(urlsd)
        try:
            urllib.request.urlopen(urlsd)
            check = urllib.request.urlopen(urlsd)
            mdata = int(check.info()['Content-Length']) #get metadata
            datemod = check.info()['Last-Modified']
            if mdata > 1073741824:
                size = round(float((((int(mdata)/1024)/1024)/1024)),2) # B -> KB -> MB -> GB
                msg = "@everyone JMS ver.{} Patch is up!\n\nPatch Size is: {}GB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            else:
                size = round(float((int(mdata)/1024)/1024),2) # B -> KB -> MB
                msg = "@everyone JMS ver.{} Patch is up!\n\nPatch Size is: {}MB\nDate uploaded: {}\nLink: {}".format(newver, size, datemod, urlsd)
            newver+=1
            await client.get_channel(###Channel ID ###).send(msg)
            if down == 1:
                filename = "00{}to00{}.patch".format(oldver, newver)
                print("Downloading...")
                urllib.request.urlretrieve(urlsd, filename)
                print("Download Complete.")
            await asyncio.sleep(10)
            open('ver.txt', 'w').close()
            oldver+=1
            x = open("ver.txt", "w")
            x.write(str(newver) + "\n")
            print("Write Complete, Killing bot")
            x.close()
            return 0
        except:
            await asyncio.sleep(50)

@client.event
async def on_ready():
    a = 0
    enable = 0 #Patch download
    while 1:
        a = int(input("\nChoose from these:\n1. KMS check\n2. KMS minor check\n3. KMST check\n4. JMS check\n5. Enable Patch Download\nChoice? : "))
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
                enable = 1;
        except:
            exit()

client.run(TOKEN)
