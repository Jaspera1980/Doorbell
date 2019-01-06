from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload
from picamera import PiCamera
from time import sleep
from datetime import datetime
import telegram

#Create camera object
camera = PiCamera()

#make 5 pictures and save them to the desktop
def five_pictures():
    camera.start_preview()
    for i in range(5):
        sleep(3)
        camera.capture('/home/pi/Pictures/image%s.jpg' %i)
    camera.stop_preview()

#Record 30 second video
def record_short_video():
    camera.start_preview()
    camera.start_recording('/home/pi/Videos/video.h264')
    sleep(30)
    camera.stop_recording()
    camera.stop_preview()

#Set up telegram bot
token_id = "<Telegram token>"
chat_id = <chat id>
bot = telegram.Bot(token=token_id)

#Send photos function
def send_photos():
    for i in range(5):
        bot.send_photo(chat_id=chat_id, photo=open("/home/pi/Pictures/image%s.jpg" %i, 'rb'))

#Google drive API to upload photos
SCOPES = 'https://www.googleapis.com/auth/drive'
#Google drive folders
folder_photos = '<folder token>'
folder_videos = '<folder token>'
#function to upload files
def upload_file(file_name, file_path, folder_id):
    #Authenticate with google api
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    #Upload files
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path,
                            mimetype='image/jpeg',
                           resumable=True)
    files = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File uploaded', '\nFile ID: %s' % files.get('id'))

#rename and move files to Google Drive
def save_photos():
    for i in range(5):
        upload_file("%s_image%s.jpg" %(datetime.now().strftime("%Y%m%d_%H%M") ,i), "/home/pi/Pictures/image%s.jpg" %i, folder_photos)

def save_videos():
    upload_file("%s_video.h264" %datetime.now().strftime("%Y%m%d_%H%M"), '/home/pi/Videos/video.h264', folder_videos)






#run functions
five_pictures()
record_short_video()
send_photos()
save_photos()
save_videos()
