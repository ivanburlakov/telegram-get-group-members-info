from dotenv import load_dotenv
load_dotenv()
import os
from telethon import TelegramClient, events, sync

targetChatTitle = os.environ.get("CHAT_TITLE")
apiID = int(os.environ.get("API_ID"))
apiHash = os.environ.get("API_HASH")

client = TelegramClient('me', apiID, apiHash)
client.start()

dialogs = client.get_dialogs()
chatID = client.get_entity(targetChatTitle).id
members = client.get_participants(chatID)

membersStr = ''
counter = 1

if not os.path.exists('./photos'):
    os.makedirs('./photos')

for user in members:
    row = '{}: {}, {} - {}, {}\n\n'.format(counter, user.first_name, user.last_name, user.phone, user.username)

    photoCounter = 1

    for photo in client.iter_profile_photos(user):
        fileName = client.download_media(photo, './photos')
        os.rename(r'{}'.format(fileName),r'./photos/{}-{}.jpg'.format(user.id, photoCounter))
        photoCounter += 1
    membersStr += row
    counter += 1

with open('members.txt', 'w', encoding='utf-8') as file:
    file.write(membersStr)