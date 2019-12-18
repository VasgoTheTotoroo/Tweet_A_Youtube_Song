#Version 2.0 create by Vassia Bonandrini
#Last release : 12/12/2019

import json
import urllib.request
import random
import time
import tweepy
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import *
from selenium.webdriver.common.keys import Keys
#import autoit for windows
import pyautogui

while(True):	
	starttime=time.time()
	count =50
	API_KEY = ''
	cx=''
	searchTerm="lofi"
	videoId=""
	contenu=""
	contenuP=""
	page=""
	PageP=1
	imageSearch=("Ghibli%20Wallpaper")
	num=1
	LINK=""
	PHOTO=""
	NOM_VID=""
	waittime=3600.0*24
	driverpth = "/usr/lib/chromium-browser/chromedriver"
	#photopath = ["Desktop","TotoroXLofi","avatar.jpg"] for windows
	
	user_insta=''
	passwd_insta=''

	OAUTH_TOKEN = ""
	OAUTH_SECRET = ""
	CONSUMER_KEY = ""
	CONSUMER_SECRET = ""
	TWITTER_HANDLE = "Totoro_X_Lofi"

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(OAUTH_TOKEN,OAUTH_SECRET)

	api=tweepy.API(auth)

	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")

	##download photos

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
		print("Le programme se ferme, en attente du changement des mots clés")
		break


	##Youtube link

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
		
	#post on twitter
	
	api.update_with_media(PHOTO,NOM_VID+" #lofi #study #chill #totoro #Ghibli "+LINK)
	print("Dernier tweet posté sur mon compte:\n"+api.user_timeline(id=1173918448855990272,count=1)[0].text)
	
	#post on instagram
	
	options = Options()
	options.add_argument("--log-level=3")
	options.add_argument("--silent")
	#options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-logging")
	options.add_argument("--mute-audio")
	#mobile_emulation = {"deviceName": "Nexus 5"}
	#options.add_experimental_option("mobileEmulation", mobile_emulation)
	options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
	driver = webdriver.Chrome(executable_path=driverpth,options=options)
	driver.get("https://www.instagram.com/accounts/login/?hl=fr")
	time.sleep(3)
	driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/form/div[4]/div/label/input").send_keys(user_insta)
	time.sleep(0.5)
	driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/form/div[5]/div/label/input").send_keys(passwd_insta)
	time.sleep(0.5)
	driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/form/div[7]/button/div").click()
	while 1:
		time.sleep(1)
		try:
			driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/button").click()
			break
		except:
			pass
	while 1:
		time.sleep(1)
		try:
			driver.find_element_by_xpath("//button[contains(text(),'Annuler')]").click()
			break
		except:
			pass
		#depends if you have the window for notification when you open chrome
	# while 1:
		# time.sleep(1)
		# try:
			# driver.find_element_by_xpath("//button[contains(text(),'Plus tard')]").click()
			# break
		# except:
			# pass

	driver.find_element_by_xpath("//div[@role='menuitem']").click()
	time.sleep(2)
	pyautogui.press('enter')
	time.sleep(2)
	pyautogui.press('enter')
	time.sleep(2)
	pyautogui.press('enter')
	time.sleep(5)

	#Works only in windows
	# autoit.win_active("Ouvrir") #open can change by your os language if not open change that
	# time.sleep(2)
	# autoit.control_send("Ouvrir", "Edit1", photopath[0])
	# time.sleep(1.5)
	# autoit.control_send("Ouvrir", "Edit1", "{ENTER}")
	# time.sleep(1.5)
	# autoit.control_send("Ouvrir", "Edit1", photopath[1])
	# time.sleep(1.5)
	# autoit.control_send("Ouvrir", "Edit1", "{ENTER}")
	# time.sleep(1.5)
	# autoit.control_send("Ouvrir", "Edit1", photopath[2])
	# time.sleep(1.5)
	# autoit.control_send("Ouvrir", "Edit1", "{ENTER}")
	#time.sleep(2)


	driver.find_element_by_xpath("//*[@id='react-root']/section/div[1]/header/div/div[2]/button").click()
	time.sleep(5)
	pyautogui.moveTo(200,240)
	time.sleep(1)
	pyautogui.click()
	time.sleep(1)
	pyautogui.typewrite(NOM_VID+" #lofi #study #chill #totoro #Ghibli "+LINK)
	time.sleep(1)
	#driver.find_element_by_xpath("//*[@id='react-root']/section/div[2]/section[1]/div[1]/textarea").send_keys(phototext)
	time.sleep(5)
	driver.find_element_by_xpath("//button[contains(text(),'Partager')]").click()
	time.sleep(5)
	driver.close()
		
	os.remove(PHOTO)
	time.sleep(waittime- ((time.time() - starttime) % waittime))
