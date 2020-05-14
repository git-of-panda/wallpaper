import os
from bs4 import BeautifulSoup
import requests
import subprocess
import re
import random
import json

class text_colours:
    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    bold = '\033[1m'
    reset = '\u001b[0m'

def config_check():
    # get current directory so we can use absolute paths
    cwd = os.path.dirname(os.path.realpath(__file__))
    config_file = cwd+"\\wallpaper_settings.cfg"

    # check for the config file
    if os.path.exists(config_file):
        print("Config file exists")
        config_parse(config_file)
    else:
        create_config(config_file)

def config_parse(config_file):
    cf = open(config_file, 'r')

    # use bool to track if we're in the subreddit section
    subreddit_bool = False
    subreddit_list = []

    # go through config file
    for line in cf.readlines():
        # get list of subreddits
        if "Subreddit List" in line:
            subreddit_bool = True

        if subreddit_bool is True:
            if '#' not in line:
                subreddit = re.findall(r'"(.*?)"', line)
                subreddit_list = subreddit_list + subreddit
        elif "]":
            subreddit_bool = False
        
        # get download location
        if "Download Directory" in line:
            download_directory = line.split()[-1]
        
        # Number of monitors
        if "Number of monitors" in line:
            no_of_monitors = int(line.split()[-1])
        
        # different wallpaper per monitor
        if "Unique wallpaper per monitor" in line:
            unique_per_monitor = line.split()[-1]
    
    if unique_per_monitor:
        chosen_subs = random.sample(subreddit_list, k=no_of_monitors)
    else:
        chosen_subs = random.choice(subreddit_list)
    
    get_picture_url(chosen_subs, no_of_monitors)


def get_picture_url(chosen_subs, no_of_monitors):
    # Spoof connection as Firefox in order to get back what we want
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'}

    #chosen_subs = ["/r/ArtefactPorn"]

    # get the link of the top picture of the week
    for subreddit in chosen_subs:
        url = "https://old.reddit.com/%s/top/?sort=top&t=week" % subreddit
        print("Getting HTML code from %s for sub %s" % (url, subreddit))
        html_page = requests.get(url, headers=headers)

        # 200 = web page request was successful
        if html_page.status_code == 200:
             # Parse HTML for Beautiful Soup
            reddit_soup = BeautifulSoup(html_page.content, 'html.parser')
            
            # Get the submission title as we'll use this to search for the URL
            top_post = reddit_soup.find('div', {"data-type": "link"})
            top_post_title = top_post.find('a', {"class": "title"}).text
            top_post_link = top_post["data-url"]
            
            print("Title: %s\nLink: %s" % (top_post_title, top_post_link))
            
            download_picture(top_post_link)
        else:
            print("Unsuccessful in getting the HTML from %s. HTTP response: %s" % (url, html_page.status_code))
            exit(1)

def download_picture(download_link):
    print("Downloading from %s" % download_link)

def create_config(config_file):
    print("File not found, assuming first run, creating new config file: \"%s\"" % config_file)
    
    # set variables first
    picture_location_root = "C:\\Users\\%s\\Pictures" % user
    picture_location_dir = "C:\\Users\\%s\\Pictures\\wallpaper" % user

    # Get download directory from user
    download_path = wallpaper_directory(picture_location_root, picture_location_dir)
    urls = ["https://www.reddit.com/r/ImaginaryNetwork/wiki/networksublist", "https://www.reddit.com/r/sfwpornnetwork/wiki/network", "https://old.reddit.com/user/ImaginaryMod/m/imaginaryexpanded/"]
    list_of_subreddits = get_html(urls)
    
    monitors, different_wallpapers = numbers_monitors()
    
    # Write everything to config file
    print("Writing to config file")
    with open(config_file, 'w') as cf:
        cf.write("Download Directory: %s\n" % download_path)
        cf.write("Number of monitors: %s\n" % monitors)
        cf.write("Unique wallpaper per monitor: %s\n" % different_wallpapers)
        
        cf.write("Subreddit List: [")
        # use enumerate to be able to format the list
        for i,sub in enumerate(sorted(list_of_subreddits)):
            if i == 0:
                cf.write("\"%s\",\n" % sub)
            elif i != len(list_of_subreddits) - 1:
                cf.write("\t\"%s\",\n" % sub)
            else:
                cf.write("\t\"%s\"]\n" % sub)
    print(text_colours.green + "Config file successfully written!" + text_colours.reset)

def wallpaper_directory(picture_location_root, picture_location_dir):
    # Let's see if the default Picture folder exists
    if os.path.exists(picture_location_root):
        location_confirm = input("Do you want to use %s as the wallpaper folder? (Y/n)" % picture_location_dir)
        location_confirm = location_confirm.capitalize()

        # Happy to use the default position
        if location_confirm == "Y" or location_confirm == "" or location_confirm == "Yes":
            print("Using %s as wallpaper folder..." % picture_location_dir)
        # New position picked
        elif location_confirm == "N" or location_confirm == "No":
            picture_location_dir = input("Please enter fullpath for wallpaper storage: ")

            # Use backslash escaping for Python
            if picture_location_dir.count("\\") == '1':
                picture_location_dir = picture_location_dir.replace("\\", "\\\\")

            print("Checking supplied location %s" % picture_location_dir)

            # Check directory exists
            if not os.path.exists(picture_location_dir):
                create_confirm = input("%s doesn't exist, create? Y/n")
                if create_confirm == "y" or create_confirm == "Y" or create_confirm == "yes" \
                or create_confirm == "" or create_confirm == "Yes":
                    os.mkdir(picture_location_dir)
                else:
                    pass
            else:
                print("Directory exists, continuing")
        # Gibberish was entered, reprompt:
        else:
            wallpaper_directory(picture_location_root, picture_location_dir)
    
    else:
        print("Default Pictures folder doesn't exist")
        picture_location_dir = input( "Please enter fullpath for wallpaper storage:")

    return picture_location_dir

def get_html(urls):
    # Spoof connection as Firefox in order to get back what we want
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'}

    # list to hold URLs
    url_links = []
    
    # query both URLs
    for url in urls:
        if "ImaginaryMod" in url:
            # There is an 18+ check the first time we access the Expanded Imaginary site.
            # Use cookies to set that we already verified
            cookies_jar = requests.cookies.RequestsCookieJar()
            cookies_jar.set('over18', '1', domain='.reddit.com', path='/')
            html_page = requests.get(url, headers=headers, cookies=cookies_jar)
        else:
            # No need for cookies otherwise
            html_page = requests.get(url, headers=headers)

        # 200 = web page request was successful
        if html_page.status_code == 200:
            print("Getting list from %s" % url)
            if "ImaginaryMod" in url:
                subreddit_links = get_links(html_page, url)
            else:
                subreddit_links = get_links(html_page)
            url_links = url_links + subreddit_links
        else:
            print(text_colours.red + "Unsuccessful in getting the HTML from %s. HTTP response: %s" % (url, html_page.status_code) + text_colours.reset)
            exit(1)

    # Add in some manually that we like
    url_links.append("/r/wallpaper")
    url_links.append("/r/wallpapers")
    
    return url_links
    
def get_links(html_page, url=None):
    # Convert HTML and search for all hyperlinks
    reddit_soup = BeautifulSoup(html_page.content, 'html.parser')
    
    # Expanded Imaginary page has different parsing for the list
    if url:
        list_of_subs = reddit_soup.find('ul', {"class": "subreddits"})
        links = list_of_subs.find_all('a', href=True)
    else:
        links = reddit_soup.find_all('a', href=True)
    
    # Create list to hold links
    subreddit_links = []

    # Loop through and add any with /r/ into the list
    for l in links:
        if "/r/" in l.text:
            subreddit_links.append(l.text)
    
    return subreddit_links

def numbers_monitors():
    # I could only get this to run in a bat file. Get number of monitors
    p = subprocess.Popen("monitor.bat", stdout=subprocess.PIPE, shell=True)
    stdout = p.communicate()
    no_monitors = int(stdout[0])

    # Prompt if they want a different wallpaper on each screen
    if no_monitors > 1:
        unique_backgrounds = input("There are %s monitors, do you want a different image on each monitor? (y/N)" % no_monitors)

        if unique_backgrounds.capitalize().startswith("Y"):
            unique = "yes"
        else:
            unique = "no"
    else:
        unique = "no"
    return no_monitors, unique


if __name__ == "__main__":
    # set global variables
    user_info = os.popen("whoami")
    for output in user_info:
        domain = output.split("\\")[0].strip()
        user = output.split("\\")[1].strip()
    
    config_check()