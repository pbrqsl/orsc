from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# options = Options()
# options.add_argument("window-size=1400,600")
# options.add_extension(r'D:\python_home\chrome_addons\oreilly\1.0.13_0.crx')
#
# s = Service('D:\python_home\chromedriver_win32\chromedriver.exe')
# chrome = webdriver.Chrome(service=s, options=options)
#
# chrome.get('https://google.com')
# time.sleep(2)
# url = chrome.current_url

#print(url)

url = 'https://learning.oreilly.com/videos/python-game-development/9781771374071/9781771374071-video221030/'
print(url.split('/')[5])

new_json_structure = {'course_id': ['course_title', []]}