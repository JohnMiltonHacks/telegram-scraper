from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import time,os,sys,json,random,csv
r= "\u001b[31;1m "
a= "\u001b[32m "
y = "\u001b[33;1m "
b="\u001b[34;1m "
m="\u001b[35;1m "
c=" \u001b[36;1m "
clear = lambda:os.system('clear')
clear()
inf = (y+'T'+a+'E'+b+'L'+y+'E'+m+'G'+c+'R'+r+'A'+y+'M'+'  '+y+'S'+a+'C'+b+'R'+y+'A'+m+'P'+c+'E'+r+'R'+y+'  '+'2'+y+'0'+a+'2'+b+'1'+y+'  '+m+'B'+c+'Y'+r+'  '+y+'J'+'O'+y+'H'+a+'N'+b+'  '+y+'M'+m+'I'+c+'L'+r+'T'+y+'O'+'N')
print(inf)
print("")
print("")
if os.path.isfile('my_log.txt'):
    with open('my_log.txt', 'r') as r:
        data = r.readlines()
    api_id = data[0]
    api_hash = data[1]

else:
    api_id = input('Enter api_id: ')
    api_hash = input('Enter api_hash: ')
    with open('my_log.txt', 'w') as a:
        a.write(api_id + '\n' + api_hash )
client = TelegramClient('JohnMilton', api_id, api_hash)
client.start()
clear()
print(inf)
print('')
print('')
chats = []
last_date = None
chunk_size = 200
groups=[]
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
for chat in chats:
    try:
        if True:
            groups.append(chat)
    except:
        continue
print(y+'Choose a group/channel to scrape members from:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1
g_index = input(y+'Enter a number (or press ENTER to skip): ')
if g_index == '' :
    clear()
    print(inf)
    print('')
    print('')
    print(y+"Ok. skipping...")
    time.sleep(1)
else:
    clear()
    print(inf)
    print('')
    print('')
    target_group=groups[int(g_index)]
    print(y+' Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)
    print('Saving In file...')
    with open("members.csv","w",encoding='UTF-8') as f:
        writer=csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
    print(a+'Members scraped successfully.')
    time.sleep(1)
clear()
print(inf)
print('')
print('')
input_file = "members.csv"
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['name'] = row[3]
        users.append(user)


chats = []
last_date = None
chunk_size = 200
groups=[]
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if True:
            groups.append(chat)
    except:
        continue

print('Choose a group/channel to add members:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input('Enter a Number: ')
my_participants = client.get_participants(groups[int(g_index)])
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
my_participants_id = []
for my_participant in my_participants:
    my_participants_id.append(my_participant.id)
clear()
print(inf)
print('')
print('')

q=0
n = 0

for user in users:
    n += 1
    if n % 20 == 0:
        print (y+'waiting for 1 minute to avoid flooding')
        time.sleep(60)
    elif n>= 200:
        client.disconnect()
        break
    elif q>= 20:
        client.disconnect()
        break
    if user['id'] in my_participants_id:
        print(a+'User already present,skipping...')
        q=0
        continue
    try:
        print (a+'Adding {}'.format(user['name']))
        if True :
            if user['username'] == "":
                continue
        user_to_add = client.get_input_entity(user['username'])
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print(a+'Waiting for 3-5 Seconds...')
        time.sleep(random.randrange(3,5))
    except PeerFloodError:
        print('\u001b[31;1mGetting Flood Error from telegram. Script is stopping now. Please try again after some time.')
        q+= 1
    except UserPrivacyRestrictedError:
        print('\u001b[31;1mThe user\'s privacy settings do not allow you to do this. Skipping.')
        q= 0
    except UserBotError:
        print('\u001b[31;1mCan\'t add Bot. Skipping...')
        q= 0
    except InputUserDeactivatedError:
        print('\u001b[31;1mThe specified user was deleted. Skipping...')
        q= 0
    except UserChannelsTooMuchError:
        print('\u001b[31;1mUser in too much channel. Skipping.')
    except UserNotMutualContactError:
        print('\u001b[31;1mMutual No. Skipped.')
        q = 0
    except Exception as e:
        print('\u001b[31;1mError:', e)
        print('Trying to continue...')
        q += 1
        continue
    except:
        traceback.print_exc()
        print('\u001b[31;1mUnexpected Error')
        q=0
        continue
