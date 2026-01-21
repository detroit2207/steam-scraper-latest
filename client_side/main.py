import requests
import re
import sys
import subprocess
from bs4 import BeautifulSoup
import time

########################## getting slug name from server code ##################################
ENDPOINT = "https://steam-scraper-six.vercel.app/search"

def search(query):
    try:
        response = requests.get(ENDPOINT,params={"query":query})
        if(response.status_code==200):
            data = response.json()
        
        return [game['slug'] for game in data.get("results",[])]
    
    except Exception as e:
        print(f"error:{e}")
        return []

query = input("Enter a game name:")

suggestions = search(query)

display_lines = [slug for slug in suggestions]

# print(display_lines)

process = subprocess.Popen(
    ["fzf",'--height=10','--border','--prompt=Select game'],
    stdout=subprocess.PIPE,
    stdin=subprocess.PIPE,
    text=True
)

selected,_=process.communicate('\n'.join(suggestions))

# print(selected)

##########################################################################################

####################################### scraping credentials from pokopow ##########################################
url = f"https://pokopow.com/{selected.strip()}"

# print(url)

html = requests.get(url).text

soup = BeautifulSoup(html,"html.parser")

text = soup.get_text(separator="\n")
# print(text)

usernames = re.findall(r'USER : (\S+)',text)
passwords = re.findall(r'PASS : (\S+)',text)

import subprocess

for username, password in zip(usernames, passwords):
    print("\nUsername:", username)
    print("Password:", password)



    try:
        steam_process = subprocess.Popen(
        ["steamcmd", "+login", username, password, "+quit"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,   # merge stderr into stdout
        stdin=subprocess.DEVNULL,
        text=True,
        bufsize=1,             # line-buffered
        )


        output, _ = steam_process.communicate(timeout=30)

        if "Waiting for user info...OK" in output:
            print(f"[SUCCESS] {username}")

        elif "Steam Guard" in output:
            print(f"[STEAM GUARD] {username}")

        elif "Invalid Password" in output :
            print(f"[INVALID PASSWORD] {username}")

        else:
            print(f"[UNKNOWN RESULT] {username} {output}")
    
    except subprocess.TimeoutExpired:
        steam_process.kill()
        print("Login process timed out.")

    except Exception as e:
        print(f"{username} : {e}")

    time.sleep(3)   

#################################################################################################
