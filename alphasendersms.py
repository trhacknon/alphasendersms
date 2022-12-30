#!/usr/bin/python3
import sys,random,time,os,re
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
  rez = os.mkdir('Logs')
  rez = r'Logs'
except:
  rez = r'Logs'
try:
    from colorama import Fore, Back, init
    init (autoreset = True)
except ImportError:
    os.system('pip install colorama')
    from colorama import Fore, Back, init
    init (autoreset = True)
try:
    import requests
    from requests.auth import HTTPBasicAuth
    
except ImportError:
    os.system('pip install requests')
    import requests
    from requests.auth import HTTPBasicAuth
try:
    from prettytable import PrettyTable
except ImportError:
    os.system('pip install prettytable')
    from prettytable import PrettyTable


rr,bb,cc,ww,yy,gg = Fore.RED,Fore.BLUE,Fore.CYAN,Fore.WHITE,Fore.YELLOW,Fore.GREEN
cc = [rr,bb,cc,ww,yy,gg]
sent,failed,left,balance = 0,0,"",""
def succ(stat):
	with open(os.path.join(rez,'Sent'),'a+') as filee:
             filee.write(stat.strip()+'\n')
def fail(stat):
	with open(os.path.join(rez,'Failed'),'a+') as filee:
             filee.write(stat.strip()+'\n')   

def tracker(numb):
    global sent
    global failed
    global left
    global balance
    x = PrettyTable() 
    x.field_names = [f"{random.choice(cc)}SENDING TO", f"{random.choice(cc)}SENT", f"{random.choice(cc)}FAILED", f"{random.choice(cc)}REMAINING",f"{random.choice(cc)}BALANCE"]
    x.add_row([numb, sent, failed, left,balance])
    print(x)  
    time.sleep(random.uniform(0.1, 1))
    sys.stdout.write("\033[5A")  
         
def karix(acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    inf = (str(acc_id),str(acc_tok))
    intel = {"channel": "sms","source": str(sender_id),"destination": [str(numb)],"content": {"text": str(message)}}
    message = ses.post('https://api.karix.io/message/',json=intel , auth = inf)
    try:
     search = re.search('"status":"queued"', message.text)
     search1 = re.search('"status":"sent"', message.text)
     search2 = re.search('"status":"delivered"', message.text)
     bal = message.json()
     balance = str(bal['meta']['available_credits'])
    except Exception as e:
       pass  
    try:
     if  search1 or search or search2 :
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e)  
      
      
def telesign (acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    inf = (str(acc_id),str(acc_tok))
    intel = {"message": str(message),"from": str(sender_id),"message_type": 'ARN',"phone_number": str(numb)}
    message = ses.post('https://rest-api.telesign.com/v1/messaging',data=intel , auth = inf)
    search = re.search('"status": {"code": 290', message.text)
    try:
     if  search :
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e)  
     

def nexmo (acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    try:
     import nexmo
    except ImportError:
       os.system('pip install nexmo')
       import nexmo
    client = nexmo.Sms(key=str(acc_id), secret=str(acc_tok))
    data = client.send_message({'from': str(sender_id), 'to': str(numb), 'text': str(message)})
    ba = nexmo.Client(key=str(acc_id), secret=str(acc_tok))
    balance = ba.get_balance()['value']
    try:
     if data['messages'][0]['status'] == '0':
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e)  

def textbelt(acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    intel = {
    "phone": str(numb),
    "message": str(message),
    "key": str(acc_tok)
          
       }
    message = ses.post('https://textbelt.com/text',json=intel)
    bal = message.json()
    balance = str(bal['quotaRemaining'])
    try:
     if str(bal['success']).lower() == 'true' :
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e) 

def SMS77(acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    intel = {
    "p": str(acc_id),
    "to": str(numb),
    "text": str(message),
    "from": str(sender_id)
          
       }
    message = ses.post('https://gateway.sms77.io/api/sms',params=intel)
    bal = ses.get(f'https://gateway.sms77.io/api/balance?p={str(acc_id)}')
    balance = bal.text
    try:
     if message.status_code == 100 :
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e) 


def smsbeep(acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    intel = {"username":str(acc_id),"apikey": str(acc_tok),"sender": str(sender_id),"messagetext": str(message),"flash": "0","recipients": str(numb)}
    message = ses.get('http://api.smsbeep.com/sendsms',params=intel)
    bal = ses.get(f'http://api.smsbeep.com/balance/{str(acc_id)}/{str(acc_tok)}')
    balance = bal.text
    search = re.search('SUCCESS', message.text)
    try:
     if search :
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e)


def proovl(acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
    intel = {"user": str(acc_id),"token": str(acc_tok),"from": str(sender_id),"to": str(numb),"text": str(message)}
    message = ses.post('https://www.proovl.com/api/send.php',params=intel,headers=hdr)
    bal = ses.get(f'https://www.proovl.com/api/balance.php?user={str(acc_id)}&token={str(acc_tok)}')
    balance = bal.text
    me = message.text.split(';')
    g = me[1].replace("\"","").strip()
    try:
     if me[1] != 'Authorization error':
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e)

def phcomm(acc_id,acc_tok,sender_id,numb,message):
    global sent
    global failed
    global left
    global balance
    ses = requests.session()
    intel = {"sender": str(sender_id),"content": str(message),"phone": str(numb)}
    headers = {'Authorization': 'Bearer ' +str(acc_tok)}
    message = ses.post('https://sms.phcomm.biz/api/v1/messages/send',data=intel,headers=headers)
    search = re.search('"message":"Queued Succesfully"', message.text)
    try:
     if search:
           succ(numb)
           left -= 1
           sent += 1
           tracker(numb)
    
     else:
          fail(numb)
          left -= 1
          failed += 1
          tracker(numb)        

    except Exception as e:
       print(e)
gways = [karix,telesign,textbelt,SMS77,nexmo,smsbeep,proovl,phcomm]
def logo():
    clear = "\x1b[0m"
    colors = [36, 32, 34, 35, 31, 37]
    x = """ 
   _____  .__         .__             _________                  .___            
  /  _  \ |  | ______ |  |__ _____   /   _____/ ____   ____    __| _/____________ 
 /  /_\  \|  | \____ \|  |  \\__  \  \_____  \_/ __ \ /    \  / __ |/ __ \_  __./]
/    |    \  |_|  |_> >   Y  \/ __ \_/        \  ___/|   |  \/ /_/ \  ___/|  | \/
\____|__  /____/   __/|___|  (____  /_______  /\___  >___|  /\____ |\___  >__|   
        \/     |__|        \/     \/        \/     \/     \/      \/    \/      

                  Alpha Sender V2.0 |   |  Coded by trhacknon                         
                                      
                          [+] My Telegram: @trhacknon   
         
             +-------- With Great Power Comes Great Toolz! --------+

1. Karix        4. Sms77        7.Proovl        
2. Telesign     5. Nexmo        8.Phcomm
3. Textbelt     6. Smsbeep      9.About Me
                                     """
    for N, line in enumerate( x.split( "\n" ) ):
        sys.stdout.write( " \x1b[1;%dm%s%s\n " % (random.choice( colors ), line, clear) )
        time.sleep( 0.05 )
logo()


try:
   tg = f"""-----------------------------------\nTelegram >>> https://t.me/trhacknon\n"""
   yt = f"""-----------------------------------\nYoutube  >>> https://www.youtube.com/channel/UCY9mdYNB0dPyHK826wdP32g\n"""
   tx = f"""-----------------------------------\nLet Me Know If You Need Help With Anything\n"""
   opt = int(input(f"""-----------------------------------\n{random.choice(cc)}Enter Option >>> """))
   if int(opt) == 9:
      for i in tg:
         sys.stdout.write(i)
         sys.stdout.flush()
         time.sleep(0.05)
      for i in yt:
         sys.stdout.write(i)
         sys.stdout.flush()
         time.sleep(0.05)
      for i in tx:
         sys.stdout.write(i)
         sys.stdout.flush()
         time.sleep(0.05)
      exit()
   if int(opt) not in range(1,9):exit(f"{rr}You must input a number from 1 to 6 !\n\tPlease try again")
except ValueError:
   exit(f"""-----------------------------------\n{random.choice(cc)}[+]You Need To Pick A Number""")
 
ide = input(f"""-----------------------------------\n{random.choice(cc)}[+] Enter Key , ID or Number >>> """)
key = input(f"""-----------------------------------\n{random.choice(cc)}[+] Enter Token , Password or Secret >>> """)
sender = input(f"""-----------------------------------\n{random.choice(cc)}[+] Enter Sender ID >>> """)
msg = open(input(f"""-----------------------------------\n{random.choice(cc)}[+] Enter Your Message File >>> """)).read()
pho = open(input(f"""-----------------------------------\n{random.choice(cc)}[+] Enter Phone Numbers List >>> """)).read().splitlines()
th = int(input(f"""-----------------------------------\n{random.choice(cc)}[+]Enter number of threads >>> """))
left = len(pho)
try:
    with ThreadPoolExecutor(th) as executor:
      for phonen in pho:
        executor.submit(gways[int(opt)-1],ide,key,sender,phonen.strip(),msg)
except Exception as e:
      print(e)

