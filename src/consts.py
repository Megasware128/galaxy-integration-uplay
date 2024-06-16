import os
from definitions import System, SYSTEM
import re
import requests
from bs4 import BeautifulSoup

UBISOFT_REGISTRY = "SOFTWARE\\Ubisoft"
STEAM_REGISTRY = "Software\\Valve\\Steam"
UBISOFT_REGISTRY_LAUNCHER = "SOFTWARE\\Ubisoft\\Launcher"
UBISOFT_REGISTRY_LAUNCHER_INSTALLS = "SOFTWARE\\Ubisoft\\Launcher\\Installs"

if SYSTEM == System.WINDOWS:
    UBISOFT_SETTINGS_YAML = os.path.join(os.getenv('LOCALAPPDATA'), 'Ubisoft Game Launcher', 'settings.yml')

UBISOFT_CONFIGURATIONS_BLACKLISTED_NAMES = ["gamename", "l1", '', 'ubisoft game', 'name']

CHROME_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"

# Fetching the HTML content from the URL
ids_url = 'https://ubisoftconnect.com/invalid'
ids_response = requests.get(ids_url)

# Parsing the HTML content
soup = BeautifulSoup(ids_response.content, 'html.parser')

# Extracting the attributes directly from the global-navigation tag
navigation_tag = soup.find('global-navigation')

if navigation_tag:
    CLUB_APPID = navigation_tag.get("app-id")
    CLUB_GENOME_ID = navigation_tag.get("genome-id-emea")
else:
    CLUB_APPID = ''
    CLUB_GENOME_ID = ''

AUTH_PARAMS = {
    "window_title": "Login | Ubisoft WebAuth",
    "window_width": 460,
    "window_height": 690,
    "start_uri": f"https://connect.ubisoft.com/login?appId={CLUB_APPID}&genomeId={CLUB_GENOME_ID}&lang=en-US&nextUrl=https:%2F%2Fconnect.ubisoft.com%2Fready",
    "end_uri_regex": r".*rememberMeTicket.*"
}

def regex_pattern(regex):
    return ".*" + re.escape(regex) + ".*"


AUTH_JS = {regex_pattern(r"connect.ubisoft.com/ready"): [
            r'''
            window.location.replace("https://connect.ubisoft.com/change_domain/"); 

            '''
        ],
            regex_pattern(r"connect.ubisoft.com/change_domain"): [
            r'''
            window.location.replace(localStorage.getItem("PRODloginData") +","+ localStorage.getItem("PRODrememberMe") +"," + localStorage.getItem("PRODlastProfile"));

            '''
        ]}

