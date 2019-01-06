from gpiozero import Button
from time import sleep
from datetime import datetime
import telegram
import paramiko

#automatic startup
print("Starting Button program with 20 seconds delay")
sleep(20)
print("Button program is ready")

#Set GPIO pin to button
button = Button(18)

#Set counter
counter = 0

#open log_file or create one if it not exists
log_file = open("log_file.txt", "a+")

#Remote script activation
HOSTNAME = '<ip address>'
PORT = 22
USERNAME = '<username>'
PASSWORD = '<password>'
COMMAND = 'python3 Camera_script.py'

def take_photos():
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.load_system_host_keys()
    sshClient.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
    sshClient.exec_command(COMMAND)
    print("camera activated")

#Set up telegram bot
token_id = "<Telegram token>"
chat_id = <chat id>
bot = telegram.Bot(token=token_id)


#loop for actions when button is pressed
try:
    while True:
        if button.is_pressed:
            counter = counter + 1
            print("Pressed %s" %counter)
            print(datetime.now())
            #write button press to log file
            log_file.write((str(datetime.now())+ "\n"))
            #Take photos
            take_photos()
            #Send telegram message
            bot.send_message(chat_id=chat_id, text="Er heeft iemand heeft aangebeld om %s" %datetime.now().strftime("%H:%M"))
            print("Telegram message send")
        sleep(1)

finally:
    log_file.close()
