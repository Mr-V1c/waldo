from bs4 import BeautifulSoup as bs
import requests
import os
from datetime import datetime
import sys
import getopt
from random import randint

# To log data of the downloads
frmt = "%d-%m-%Y"
todays_date = datetime.now().strftime(frmt)
# Path to logs
path_to_logs = "./log.text"
# random wallpapers source
url = "https://wallhaven.cc/search?categories=110&purity=100&atleast=1920x1080&sorting=random&order=asc&ai_art_filter="


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dh")
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(2)
    if args != []:
        print(f"This script takes no agrs and {len(args)} was/were given.")
        sys.exit(2)
    for opt, _ in opts:
        if opt == "-d":
            check_log()
        elif opt == "-h":
            usage()
            sys.exit()
    download()


def usage():
    print(
        f"""Usage: {sys.argv[0]} [option]
       Options:
       -d       : daily downloads; checks internal logs to ensure only a download per day"""
    )


def check_log():
    if os.path.exists(path_to_logs):
        with open(path_to_logs, "r") as f:
            if todays_date == f.readline(-1).split(",")[1].strip():  # logs_date
                print("There is already a download today")
                sys.exit()


def download():
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    index = randint(0, 10)
    # print(len(soup.find_all("a",class_="preview")))#-- 24 preview links consistently
    previews = soup.find_all("a", class_="preview")[index]["href"]
    full_res_address = requests.get(previews)
    image_page = bs(full_res_address.text, "html.parser")  # full image resolution page
    # print(image_page.find_all("img")[2]["src"]
    full_res_image = image_page.find("img", id="wallpaper").attrs["src"]
    os.system(f"wget {full_res_image} -P ~/Pictures/wallpapers/")
    with open("log.text", "a") as f:
        f.write(f"{full_res_image} , {todays_date}\n")


if __name__ == "__main__":
    main()
