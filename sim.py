from telethon import TelegramClient, events, sync
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import time,os,random,csv,sys
r= "\u001b[31;1m"
a= "\u001b[32m"
y = "\u001b[33;1m"
b="\u001b[34;1m"
m="\u001b[35;1m"
c="\u001b[36;1m"
clear = lambda:os.system('clear')
inf = (y+'T'+a+'E'+b+'L'+y+'E'+m+'G'+c+'R'+r+'A'+y+'M'+'  '+y+'S'+a+'C'+b+'R'+y+'A'+m+'P'+c+'E'+r+'R'+y+'  '+'2'+y+'0'+a+'2'+b+'1'+y+'  '+m+'B'+c+'Y'+r+'  '+y+'J'+'O'+y+'H'+a+'N'+b+'  '+y+'M'+m+'I'+c+'L'+r+'T'+y+'O'+'N')
def info():
    clear()
    print(inf)
    print("")
    print("")
info()
def ospath():
    o=int(input(b+" How many telegram accounts do you have ? : "))
    for po in range(o):
        if os.path.isfile('multi_log.txt'):
            with open('multi_log.txt', 'r') as f:
                data = f.readlines()
            v=int(((len(data))/2))
            z=v
        else:
            z=0
        api_id= input(b+' Enter api_id_{}: '.format(z+1))
        api_hash= input('Enter api_hash_{}: '.format(z+1))
        with open('multi_log.txt', 'a') as f:
            f.write(api_id+'\n'+api_hash+'\n')
        client = TelegramClient("JohnMilton{}".format(z), api_id, api_hash)
        client.start()
        time.sleep(1)
        info()
        client.disconnect()
if os.path.isfile('multi_log.txt'):
    print(a+"                (y/n)            ")
    xc=input(c+" Do u want to continue the last session ? ")
    if xc=='y':
        cy=input("Do u want to add still more telegram accounts with this scraper ? ")
        if cy=='y':
            ospath()
        else:
            pass
    else:
        cv=input("Do u want to remove the last session ? ")
        if cv=='y':
            with open('multi_log.txt', 'r') as f:
                data = f.readlines()
            v=int((len(data))/2)
            con=input(r+" Are you sure to permanently delete all files related to last session ? ")
            if con=='':
                print(m+" U 've pressed Enter,Now exiting..."+'\n'+a+"No files were deleted ! ")
                sys.exit(1)
            elif con=='y':
                print(r+ " Now deleting files related to last session")
                time.sleep(1)
                for d in range(v-1):
                    os.remove("JohnMilton{}.session".format(d))
                os.remove('multi_log.txt')
            ospath()
        else:
            sys.exit()

else:
    ospath()

with open('multi_log.txt', 'r') as f:
    data = f.readlines()
v=int((len(data))/2)
t=0
api_id = data[t]
api_hash = data[t+1]
client = TelegramClient("JohnMilton{}".format(t), api_id, api_hash)
client.start()
t+=2
info()
x=1
for s in range(v):
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
    print(b+' Choose a group/channel to scrape members from:')
    i=0
    for g in groups:
        print(m+str(i) +y+ ' - '+a + g.title)
        i+=1
    g_index = input(b+' Enter a number (or press ENTER to skip): ')
    if g_index == '' :
        info()
        print(m+" Ok. skipping...")
        time.sleep(1)
    else:
        info()
        target_group=groups[int(g_index)]
        print(y+' Fetching Members...')
        all_participants = []
        all_participants = client.get_participants(target_group, aggressive=True)
        print(y+' Saving In file...')
        with open("Members.csv","a",encoding='UTF-8') as f:
            writer=csv.writer(f,delimiter=",",lineterminator="\n")
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
        print(a+' Members scraped successfully.')
        time.sleep(1)
    info()
    print(b+'Choose a group/channel to add members:')
    i=0
    for group in groups:
        print(m+str(i) +y+ ' - ' +a+ group.title)
        i+=1

    g_index = input(b+' Enter a Number: ')
    if g_index=='':
        print(m+" U 've pressed Enter,Now exiting...")
        sys.exit()
    input_file = "Members.csv"
    users = []
    lines = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        for row in rows:
            lines.append(row)
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['name'] = row[3]
            users.append(user)
    my_participants = client.get_participants(groups[int(g_index)])
    target_group=groups[int(g_index)]

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
    my_participants_id = []
    for my_participant in my_participants:
        my_participants_id.append(my_participant.id)
    info()
    n,q=0,0
    for user in users:
        n += 1
        if n % 20 == 0:
            info()
            print (y+' waiting for 10 seconds to avoid flooding....')
            time.sleep(10)
        elif q>= 9:
            client.disconnect()
            if x<v:
                print(a+" now changing client...")
                api_id = data[t]
                api_hash = data[t+1]
                client = TelegramClient("JohnMilton{}".format(x), api_id, api_hash)
                client.start()
                info()
                t+=2
                x+=1
                break
            else:
                print(b+" No more clients found.Now exiting..")
                time.sleep(1)
                sys.exit()
        if user['id'] in my_participants_id:
            print(a+'User already present,skipping...')
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                for row in rows:
                    if user['id'] in row:
                        lines.remove(row)
                        
            time.sleep(1)
            continue
        try:
            print (a+' Adding {}'.format(user['name']))
            if True :
                if user['username'] == "":
                    continue
            user_to_add = client.get_input_entity(user['username'])
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print("Waiting for 2-4 Seconds...")
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                for row in rows:
                    if user['id'] in row:
                        lines.remove(row)
            with open(input_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(lines)
            time.sleep(random.randrange(2,4))
        except PeerFloodError:
            print(r+' Getting Flood Error from telegram. Script is stopping now. Please try again after some time.')
            time.sleep(1)
            q+= 1
        except UserPrivacyRestrictedError:
            print(r+' The user\'s privacy settings do not allow you to do this. Skipping.')
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                for row in rows:
                    if user['id'] in row:
                        lines.remove(row)
            time.sleep(1)
        except UserBotError:
            print(r+' Can\'t add Bot. Skipping...')
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                for row in rows:
                    if user['id'] in row:
                        lines.remove(row)

        except InputUserDeactivatedError:
            print(r+' The specified user was deleted. Skipping...')
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                for row in rows:
                    if user['id'] in row:
                        lines.remove(row)
            time.sleep(1)
        except UserChannelsTooMuchError:
            print(r+' User in too much channel. Skipping.')
            with open(input_file, encoding='UTF-8') as f:
                rows = csv.reader(f,delimiter=",",lineterminator="\n")
                for row in rows:
                    if user['id'] in row:
                        lines.remove(row)
            time.sleep(1)
        except UserNotMutualContactError:
            print(r+' Mutual No. Skipped.')
            time.sleep(1)
        except Exception as e:
            print(r+' Error:', e)
            print('Trying to continue...')
            q += 1
            time.sleep(1)
            continue


