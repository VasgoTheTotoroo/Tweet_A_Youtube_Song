from credentials import twitterOAuth
from requests import post, get
from os.path import getsize
from time import sleep
from sys import exit

TWITTER_MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
TWITTER_POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

class VideoTweet(object):
    def __init__(self, file_name):
        '''
        Defines video tweet properties
        https://github.com/twitterdev/large-video-upload-python/blob/master/async-upload.py
        '''
        self.video_filename = file_name
        self.total_bytes = getsize(self.video_filename)
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

        req = post(url=TWITTER_MEDIA_ENDPOINT_URL, data=request_data, auth=twitterOAuth)
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

            req = post(url=TWITTER_MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=twitterOAuth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                exit(0)

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

        req = post(url=TWITTER_MEDIA_ENDPOINT_URL, data=request_data, auth=twitterOAuth)

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
            exit(0)

        check_after_secs = self.processing_info['check_after_secs']
        
        print('Checking after %s seconds' % str(check_after_secs))
        sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = get(url=TWITTER_MEDIA_ENDPOINT_URL, params=request_params, auth=twitterOAuth)
        
        self.processing_info = req.json().get('processing_info', None)
        self.check_status()


    def tweet(self, videoName):
        '''
        Publishes Tweet with attached video
        '''
        request_data = {
            'status': videoName,
            'media_ids': self.media_id
        }

        post(url=TWITTER_POST_TWEET_URL, data=request_data, auth=twitterOAuth)