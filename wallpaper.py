import os

def config_check():
    # get current directory so we can use absolute paths
    cwd = os.path.dirname(os.path.realpath(__file__))
    config_file = cwd+"\\wallpaper_settingxs.cfg"

    # check for the config file
    if os.path.exists(config_file):
        print("Config file exists")
    else:
        create_config( config_file)

def create_config(config_file):
    print("File not found, assuming first run, creating new config file: \"%s\"" % config_file)
    
    # set variables first
    picture_location_root = "C:\\Users\\%s\\Pictures" % user
    picture_location_dir = "C:\\Users\\%s\\Pictures\\wallpaper" % user

    file_location(picture_location_root, picture_location_dir)

def file_location(picture_location_root, picture_location_dir):
    # Let's see if the default Picture folder exists
    if os.path.exists(picture_location_root):
        location_confirm = input("Do you want to use %s as wallpaper folder? (Y/n)" % picture_location_dir)
    
        # Happy to use the default position
        if location_confirm == "y" or location_confirm == "Y" or location_confirm == "yes" \
            or location_confirm == "" or location_confirm == "Yes":
            print("Using %s as wallpaper folder...")
        # New position picked
        elif location_confirm == "n" or location_confirm == "N" or location_confirm == "no" \
            or location_confirm == "No":
            picture_location_dir = input("Please enter fullpath for wallpaper storage: ")

            # Check directory exists
            if not os.path.exists(picture_location_dir):
                create_confirm = input("%s doesn't exist, create? Y/n")
                if create_confirm == "y" or create_confirm == "Y" or create_confirm == "yes" \
                or create_confirm == "" or create_confirm == "Yes":
                    os.mkdir(picture_location_dir)
                else:
                    
        # Gibberish was entered, reprompt:
        else:
            file_location(picture_location_root, picture_location_dir)

    else:
        print("Default Pictures folder doesn't exist")
        file_location = input( "Please enter fullpath for wallpaper storage:")
    #with open(config_file, "w") as con_fi:
    #    con_fi.write("picture_folder: %s" % picture_location_dir)


if __name__ == "__main__":
    # set global variables
    user_info = os.popen("whoami")
    for output in user_info:
        domain = output.split("\\")[0].strip()
        user = output.split("\\")[1].strip()
    
    config_check()
