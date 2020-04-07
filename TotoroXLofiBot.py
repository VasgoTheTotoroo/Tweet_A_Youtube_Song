#Version 3.0 create by Vassia Bonandrini
#Last release : 07/04/2019

import json
import urllib.request
import time
import requests
import os
from pytube import YouTube

#import for twitter
import sys
from requests_oauthlib import OAuth1

count =50
API_KEY = ''
searchTerm="lofi"
waittime=3600.0*24
time_video = 0.49 #in secondes

OAUTH_TOKEN = ""
OAUTH_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

while(True):	
	starttime=time.time()
	videoId=""
	contenu=""
	page=""
	LINK=""
	NOM_VID=""

	#get Youtube link
	print("-------------SEARCH YOUTUBE LINK-------------\n")

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
				try:
					yt=YouTube(LINK)
				except:
					continue
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

	print("-------------DOWNLOAD VIDEO-------------\n")
	t=yt.streams.filter(subtype='mp4')
	t[0].download(filename='video')

	print("-------------CUT VIDEO-------------\n")
	from moviepy.editor import *

	clip=VideoFileClip("video.mp4").subclip(0,(time_video,0))
	clip.write_videofile("temp.mp4",audio_codec='aac')
	clip.close()

	#os.remove("video.mp4")
	#post on twitter
	print("-------------Post on Twitter-------------\n")
	
	NOM_VID=NOM_VID+" #lofi #study #chill "+LINK
	MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
	POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

	oauth = OAuth1(CONSUMER_KEY,
	  client_secret=CONSUMER_SECRET,
	  resource_owner_key=OAUTH_TOKEN,
	  resource_owner_secret=OAUTH_SECRET)

	class VideoTweet(object):
		def __init__(self, file_name):
			'''
			Defines video tweet properties
			https://github.com/twitterdev/large-video-upload-python/blob/master/async-upload.py
			'''
			self.video_filename = file_name
			self.total_bytes = os.path.getsize(self.video_filename)
			self.media_id = None
			self.processing_info = None

		def upload_init(self):
			'''
			Initializes Upload
			'''
			print('INIT')

			request_data = {
			  'command': 'INIT',
			  'media_type': 'video/mp4',
			  'total_bytes': self.total_bytes,
			  'media_category': 'tweet_video'
			}

			req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
			media_id = req.json()['media_id']

			self.media_id = media_id

			print('Media ID: %s' % str(media_id))


		def upload_append(self):
			'''
			Uploads media in chunks and appends to chunks uploaded
			'''
			segment_id = 0
			bytes_sent = 0
			file = open(self.video_filename, 'rb')

			while bytes_sent < self.total_bytes:
			  chunk = file.read(4*1024*1024)
			  
			  print('APPEND')

			  request_data = {
				'command': 'APPEND',
				'media_id': self.media_id,
				'segment_index': segment_id
			  }

			  files = {
				'media':chunk
			  }

			  req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

			  if req.status_code < 200 or req.status_code > 299:
			    print(req.status_code)
			    print(req.text)
			    sys.exit(0)

			  segment_id = segment_id + 1
			  bytes_sent = file.tell()

			  print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

			print('Upload chunks complete.')


		def upload_finalize(self):
			'''
			Finalizes uploads and starts video processing
			'''
			print('FINALIZE')

			request_data = {
			  'command': 'FINALIZE',
			  'media_id': self.media_id
			}

			req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)

			self.processing_info = req.json().get('processing_info', None)
			self.check_status()

		def check_status(self):
			'''
			Checks video processing status
			'''
			if self.processing_info is None:
			  return

			state = self.processing_info['state']

			print('Media processing status is %s ' % state)

			if state == u'succeeded':
			  return

			if state == u'failed':
			  sys.exit(0)

			check_after_secs = self.processing_info['check_after_secs']
			
			print('Checking after %s seconds' % str(check_after_secs))
			time.sleep(check_after_secs)

			print('STATUS')

			request_params = {
			  'command': 'STATUS',
			  'media_id': self.media_id
			}

			req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)
			
			self.processing_info = req.json().get('processing_info', None)
			self.check_status()


		def tweet(self):
			'''
			Publishes Tweet with attached video
			'''
			request_data = {
			  'status': NOM_VID,
			  'media_ids': self.media_id
			}

			req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)

	videoTweet = VideoTweet("temp.mp4")
	videoTweet.upload_init()
	videoTweet.upload_append()
	videoTweet.upload_finalize()
	videoTweet.tweet()
		
	os.remove("temp.mp4")
	os.remove("video.mp4")
	time.sleep(waittime- ((time.time() - starttime) % waittime))
