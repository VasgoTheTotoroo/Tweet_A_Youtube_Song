#Version 4.0 created by Vassia Bonandrini vasgoduzoo@gmail.com
#Last release : 07/03/2023

from credentials import GOOGLE_API_KEY
from json import loads
from urllib.request import urlopen
from pytube import YouTube
from VideoTweet import VideoTweet
from moviepy.editor import *

MAX_RESULT = 50
SEARCH_TERM="lofi"

BEGIN_VIDEO_TIMECODE = 30 #in seconds
END_VIDEO_TIMECODE = 60

def getYoutube(googleApiKey, maxResult, searchTerms, previousLinks):
    videoId = ""
    page = ""
    youtubeLink = ""

    while(youtubeLink == ""):

        urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}&pageToken={}".format(googleApiKey, maxResult, searchTerms, page)
        webURL = urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        results = loads(data.decode(encoding))
        page = results['nextPageToken']

        for data in results['items']:
            videoId = (data['id']['videoId'])
            
            if ((videoId not in previousLinks) and (data['snippet']['liveBroadcastContent']=='none')):
                youtubeLink = "https://www.youtube.com/watch?v=" + videoId
                youtubeOject = YouTube(youtubeLink)
                youtubeTitle = data['snippet']['title']
                print(youtubeLink)
                file = open("links.txt", "a")
                file.write(videoId + "\n")
                file.close()
                break
        else:
            print("Page change\n")
            continue
        break
    return {"youtubeLink": youtubeLink, "youtubeTitle": youtubeTitle, "youtubeOject": youtubeOject}

def main():
    previousLinks=""

    print("-------------SEARCH YOUTUBE LINK-------------\n")
    file = open("links.txt", "r")
    try:
        previousLinks = file.read()
    except:
        print("The file with the previous links is empty.")
    file.close()

    youtube = getYoutube(GOOGLE_API_KEY, MAX_RESULT, SEARCH_TERM, previousLinks)
    youtubeLink = youtube["youtubeLink"]
    youtubeTitle = youtube["youtubeTitle"]
    youtubeOject = youtube["youtubeOject"]

    print("-------------DOWNLOAD VIDEO-------------\n")
    filters = youtubeOject.streams.filter(subtype = 'mp4')
    filters[0].download(filename = 'video.mp4')

    print("-------------CUT VIDEO-------------\n")
    clip = VideoFileClip("video.mp4").subclip(BEGIN_VIDEO_TIMECODE, END_VIDEO_TIMECODE)
    clip.write_videofile("temp.mp4", audio_codec='aac')
    clip.close()

    print("-------------Post on Twitter-------------\n")
    youtubeTitle = youtubeTitle + " #lofi #study #chill #beat " + youtubeLink

    videoTweet = VideoTweet("temp.mp4")
    videoTweet.upload_init()
    videoTweet.upload_append()
    videoTweet.upload_finalize()
    videoTweet.tweet(youtubeTitle)
        
    os.remove("temp.mp4")
    os.remove("video.mp4")

if __name__ == "__main__":
    main()
