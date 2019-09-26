#Version 1.0 create by Vassia Bonandrini
#Last release : 26/09/2019

import json
import urllib.request
import random
import time
import tweepy
import requests
import os

starttime=time.time()
while(True):	
	
	count =50
	API_KEY = ''
	cx=''
	searchTerm="lofi"
	videoId=""
	contenu=""
	contenuP=""
	page=""
	PageP=1
	imageSearch=("totoro%20Wallpaper")
	num=1
	LINK=""
	PHOTO=""
	NOM_VID=""

	OAUTH_TOKEN = ""
	OAUTH_SECRET = ""
	CONSUMER_KEY = ""
	CONSUMER_SECRET = ""
	TWITTER_HANDLE = ""

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(OAUTH_TOKEN,OAUTH_SECRET)

	api=tweepy.API(auth)

	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")

	##photos

	file2=open("photos.txt","r")
	try:
		contenuP=file2.read()
	except:
		print("le fichier est vide")
	file2.close()


	while(PHOTO==""):
		if(PageP>100):
			print("Tu as déjà dl toutes les photos !")
			break
		
		urlPic="https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&searchType=image&num={}&start={}&imgSize=large".format(API_KEY,cx,imageSearch,num,PageP)
		webURLPic=urllib.request.urlopen(urlPic)
		dataPic=webURLPic.read()
		encodingPic=webURLPic.info().get_content_charset('utf-8')
		resultsPic=json.loads(dataPic.decode(encodingPic))
		for data in resultsPic['items']:
			name=data['link'][-15:]
			if "/" in name:
				name=name.replace("/","_")
			if(name not in contenuP):
				print(data['link'])
				if (".jpg" not in name) and (".gif" not in name) and (".png" not in name) and (".jpeg" not in name):
					PHOTO=name+".jpg"
				else:
					PHOTO=name
				img_data = requests.get(data['link']).content
				with open(PHOTO, 'wb') as handler:
					handler.write(img_data)
				file=open("photos.txt","a")
				file.write(PHOTO+"\n")
				file.close()
		if PHOTO!="":
			break
		else:
			PageP=PageP+1
			print("changement de page, résultat de "+str(PageP)+" à "+str(PageP+1)+" !\n")
	if(PHOTO==""):
		print("Le programme se ferme, en attende du changement des mots clés")
		break


	##lien YT

	file=open("liens.txt","r")
	try:
		contenu=file.read()
	except:
		print("le fichier est vide")
	file.close()

	while(True):

		urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}&pageToken={}".format(API_KEY,count,searchTerm,page)
		webURL = urllib.request.urlopen(urlData)
		data = webURL.read()
		encoding = webURL.info().get_content_charset('utf-8')
		results = json.loads(data.decode(encoding))
		page=results['nextPageToken']

		for data in results['items']:
			videoId = (data['id']['videoId'])
			if ((videoId not in contenu) and (data['snippet']['liveBroadcastContent']=='none')):
				LINK="https://www.youtube.com/watch?v="+videoId
				NOM_VID=data['snippet']['title']
				print(LINK)
				file=open("liens.txt","a")
				file.write(videoId+"\n")
				file.close()
				break
		else:
			print("changement de page !\n")
			continue
		break
		
	api.update_with_media(PHOTO,NOM_VID+" "+LINK)
	print("Dernier tweet posté sur mon compte:\n"+api.user_timeline(id=1173918448855990272,count=1)[0].text)
	os.remove(PHOTO)
	time.sleep(3600.0 - ((time.time() - starttime) % 3600.0))