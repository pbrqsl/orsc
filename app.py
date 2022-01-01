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

my_path = r'D:\python_home\02_courses_download'
downloader_path=r'D:\python_home\yt_dl\youtube-dl.exe'

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
    print(file_prefix)
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
    dst_file = os.path.join(dst_folder, dst)
    subprocess.run([downloader_path, "--output", dst_file, url[1]])
    #except:
    #    print(f'failed with {url}')

logged_in = False

def menu():
    print(PROMPT)
    user_input = input('<get_lib>, <scrap>, <exit>: ')
    if user_input == 'get_lib':
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

        user_input = input("Navigate to any video of the course you want to scrap and enter 'go' command: ")
        if user_input == 'go':
            #chrome.get('https://learning.oreilly.com/videos/the-complete-python/9781839217289/9781839217289-video1_2/')
            vid_page = PageParser(chrome)
            time.sleep(2)
            vid_page.go_to_table()
            time.sleep(2)
            videos = vid_page.videos
            time.sleep(2)
            title = vid_page.course_title
            LinkFile.save_links(title, videos, json_links_file)
            #print(videos)
        menu()

    elif user_input == 'scrap':
        link_dict = LinkFile.read_links(json_links_file)
        print(f'currently there is {len(link_dict["links"])}')
        link_range = input('please provide the range of videos to scrap (e.g. 10-20), please note that first video has index "1": ')
        range_start = int(link_range.split('-')[0]) - 1
        range_end = int(link_range.split('-')[1])
        start_total = time.time()
        n = 0
        link_dict_range = link_dict["links"][range_start:range_end]
        for url in link_dict_range:
            start = time.time()
            print(url[1])
            index_of = str(link_dict["links"].index(url) + 1)
            dirname = link_dict["title"]
            download_episode(url, my_path, index_of, dirname)
            print(f'Download lasted {time.time() - start}')
            n += 1
        print(f'Total for {str(n)} files lasted {time.time() - start_total}')
        menu()

    elif user_input == 'exit':
        print('good bye')
        exit()
    else:
        print('unknown command')
        menu()

menu()