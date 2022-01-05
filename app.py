import time
import random
import os
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from parsers.page_parser import PageParser
import temp_dict
from filer import LinkFile
import url_links_scraper
from url_links_scraper import urls_by_id


my_path = r'D:\python_home\02_courses_download'
downloader_path= r'D:\python_home\yt_dl\youtube-dl.exe'
cookie_path = r'D:\python_home\yt_dl\96e1f6ad-3203-47eb-aa46-4581371735ea.txt'

#start chrome with installed extension
#connect to the page
#log in
# locate the course
#get the content list
#switch between the list elements
# click pause
# click download
# wait till download stops
# click get downloaded
json_links_file = 'links.json'
json_pwd_file = '_secret.json'
#jsn_pwd_file_format:
#{"username": "abc", "password": "sdasdasdasd"}
url_splitter = r'-video'

PROMPT = """
- If you want to generate the list of course videos enter 'get-lib' and follow instructions 
- If you already have the list of course videos imported please enter 'scrap' in the prompt below. 
You will be asked about range of the links to download
- enter 'exit' to exit :) 
"""

SCRAP_PROMPT = """
please provide the range of videos to scrap (e.g. "1" or "3,7-10", "11-55"),
please note that first video has index "1": """
with open(json_pwd_file, 'r') as file:
    json_creds = json.loads(file.read())

# def download_episode(url):
#     try:
#         chrome.get(url)
#         time.sleep(random.randint(4, 8))
#         page = PageParser(chrome)
#         time.sleep(random.randint(2, 6))
#         page.download_video()
#     except:
#         print(f'failed with {url}')


def download_episode(url, destination_folder, index_no, dirname="noname"):
    #try:
    print(url[1])
    file_prefix = url[1].split('/')[6]
    folder = f'{file_prefix.split("-")[0]}_{dirname}'
    dst = f'[{index_no}]_{file_prefix}_{url[0].replace(" ", "_")}.mp4'
    if os.path.isdir(os.path.join(destination_folder, folder)):
        dst_folder = os.path.join(destination_folder, folder)
    else:
        try:
            os.mkdir(os.path.join(destination_folder, folder))
            dst_folder = os.path.join(destination_folder, folder)
        except:
            pass
    down_username = 'pbrqsl@gmail.com'
    down_password = '123QWE'
    dst_file = os.path.join(dst_folder, dst)
    down_input = [downloader_path, "--output", dst_file, url[1], "--cookie", cookie_path
        , "--username"
        , down_username
        , "--password"
        , down_password]
    print(down_input)
    time.sleep(2)
    subprocess.run(down_input)
    #subprocess.run(["echo hello world"])
    #except:
    #    print(f'failed with {url}')

logged_in = False

def log_in():
    global logged_in
    if not logged_in:
        options = Options()
        options.add_argument("window-size=1400,600")
        options.add_extension(r'D:\python_home\chrome_addons\oreilly\1.0.13_0.crx')
        s = Service('D:\python_home\chromedriver_win32\chromedriver.exe')
        global chrome
        chrome = webdriver.Chrome(service=s, options=options)
        chrome.get('https://learning.oreilly.com/profile/')
        page = PageParser(chrome)
        page.login(json_creds['username'], json_creds['password'])
        time.sleep(random.randint(6, 15))
        page.click_accept_cookies()
        logged_in = True
        return chrome

def get_library(browser):
    vid_page = PageParser(browser)
    time.sleep(2)
    vid_page.go_to_table()
    time.sleep(2)
    videos = vid_page.videos
    print(videos)
    time.sleep(2)
    title = vid_page.course_title
    course_id = browser.current_url.split('/')[5]
    LinkFile.save_links(course_id, title, videos, json_links_file)

def get_id_library(course_id):
    #title = urls_by_id(course_id)[0]
    videos = urls_by_id(course_id)
    title = videos[0]
    videos = videos[1]
    print(videos)
    #title = vid_page.course_title
    #course_id = browser.current_url.split('/')[5]
    LinkFile.save_links(course_id, title, videos, json_links_file)

def get_urls():
    link_dict = LinkFile.read_links(json_links_file)
    link_dict_range = []
    finished = False
    while not finished:
        menu_item = 1
        menu_courses = {}
        for key in link_dict:
            menu_courses[str(menu_item)] = key
            print(f'{menu_item}: {key}, {link_dict[key][0]}, {len(link_dict[key][1])}')
            menu_item += 1
        while True:
            user_course_id = input('Please enter the course number (or "quit"): ')
            if user_course_id in menu_courses:
                break
            elif user_course_id == 'quit':
                return
            else:
                print('wrong choice')
                continue

        while True:
            try:
                link_range = input(SCRAP_PROMPT).split(',')
                url_indexes = ranger(*link_range)
                break
            except:
                print('wrong list')
                continue


        key = menu_courses[user_course_id]
        for index in url_indexes:
            url = link_dict[key][1][index-1]
            course_title = link_dict[key][0]
            link_dict_range.append([key, course_title, str(index), url[0], url[1]])
        user_continues = input('Do you want to add more links? <yes/no>: ')
        if user_continues == 'no':
            finished = True
    return link_dict_range


def multi_url_download(url_list):
    for item in url_list:
        start = time.time()
        url = [item[3], item[4]]
        index_of = item[2]
        dirname = item[1]
        download_episode(url, my_path, index_of, dirname)
        print(f'Download lasted {time.time() - start}')

def ranger(*args):
    range_out = []
    for arg in [*args]:
        limits = arg.split('-')
        if len(limits) == 1:
            range_out.append(int(arg))
        else:
            range_out.extend(range(int(limits[0]), int(limits[1])+1))
    return range_out

def menu():
    print(PROMPT)
    #subprocess.run([downloader_path, '--cookie 96e1f6ad-3203-47eb-aa46-4581371735ea.txt --username pbrqsl@gmail.com --password 123QWE https://learning.oreilly.com/videos/red-hat-certified/9780133929171/9780133929171-RHCE_01_02/'], capture_output=True)
    user_input = input('<get_lib>, <scrap>, <id>, <exit>: ')
    if user_input in ['get_lib', 'g']:
        chrome = log_in()
        user_input = input("Navigate to any video of the course you want to scrap and enter 'go' command: ")
        if user_input == 'go':
            get_library(chrome)
        menu()
    elif user_input in ['id', 'i']:
        user_input = input("Please enter the course ID: ")
        get_id_library(user_input)
        menu()

    elif user_input in ['scrap', 's']:
        link_dict_range = get_urls()
        if link_dict_range:
            multi_url_download(link_dict_range)
        menu()

    elif user_input == 'exit':
        print('good bye')
        exit()
    else:
        print('unknown command')
        menu()

if __name__ == '__main__':
    menu()