import requests
import re
import sys
import subprocess
from bs4 import BeautifulSoup
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


for username,password in zip( usernames,passwords ):
    print("\nUsername: ",username,"\nPassword: ",password)

#################################################################################################
