import os
from bs4 import BeautifulSoup
import requests
import subprocess
import re
import random

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
        chosen_subs = pick_subs(subreddit_list, no_of_monitors)
    else:
        chosen_subs = random.choice(subreddit_list)
    
    get_picture_url(chosen_subs, no_of_monitors)


def get_picture_url(chosen_subs, no_of_monitors):
    # get the link of the top picture of the week
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'}

    for subreddit in chosen_subs:
        url = "https://www.reddit.com/r/%s/top/?sort=top&t=week" % subreddit


def pick_subs(subreddit_list, no_of_monitors):
    chosen_subs = random.sample(subreddit_list, k=no_of_monitors)
    return chosen_subs

def create_config(config_file):
    print("File not found, assuming first run, creating new config file: \"%s\"" % config_file)
    
    # set variables first
    picture_location_root = "C:\\Users\\%s\\Pictures" % user
    picture_location_dir = "C:\\Users\\%s\\Pictures\\wallpaper" % user

    # Get download directory from user
    download_path = wallpaper_directory(picture_location_root, picture_location_dir)
    urls = ["https://www.reddit.com/r/ImaginaryNetwork/wiki/networksublist", "https://www.reddit.com/r/sfwpornnetwork/wiki/network"]
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
    print("Config file successfully written!")

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
        # get the HTML of the page
        html_page = requests.get(url, headers=headers)
        # 200 = web page request was successful
        if html_page.status_code == 200:
            subreddit_links = get_links(html_page)
            url_links = url_links + subreddit_links
        else:
            print("Unsuccessful in getting the HTML. HTTP response: %s" % html_page.status_code)
            exit(1)
    return url_links
    
def get_links(html_page):
    # Convert HTML and search for all hyperlinks
    reddit_soup = BeautifulSoup(html_page.content, 'html.parser')
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
    stdout, stderr =p.communicate()
    no_monitors = int(stdout)

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