from __future__ import unicode_literals
import youtube_dl
import json
from watson_developer_cloud import SpeechToTextV1
#IBM Watson credentials
IBM_USERNAME = "INSERT_BLUEMIX_USERNAME"
IBM_PASSWORD = "INSERT_BLUEMIX_PASSWORD"

#Get the transcript from watson and as json file
def send_to_watson():
	stt = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD, x_watson_learning_opt_out=False, use_vcap_services=False, url='INSERT_BLUEMIX_URL_FROM_DASHBOARD')
	audio_file = open("File.ogg", "rb")

	with open('result.json', 'w') as fp:
	    result = stt.recognize(audio_file, content_type="audio/ogg",
	                           continuous=True, timestamps=False,
	                           max_alternatives=1)
	    json.dump(result, fp, indent=2)

def status_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now sending to Watson ...')

# Youtube dl downlaod options
options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'progress_hooks': [status_hook],
    'outtmpl': '%(id)s.%(ext)s',
}
#Download from youtube
def download():
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download(['LINK_TO_YOUTUBE_VIDEO'])
	send_to_watson()
download()