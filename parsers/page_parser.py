import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from locators.page_locators import PageLocators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

class PageParser:
    def __init__(self, browser):
        self.browser = browser

    def login(self, username:str, password:str):
        time.sleep(random.randint(2, 4))
        email_form = self.browser.find_element(*PageLocators.EMAIL_ADDRESS_INPUT)
        email_form.click()
        actions = ActionChains(self.browser)
        time.sleep(random.randint(2, 4))
        actions.send_keys(username).perform()
        time.sleep(random.randint(2, 4))
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(random.randint(4, 6))
        actions.send_keys(password).perform()
        time.sleep(random.randint(3, 5))
        actions.send_keys(Keys.ENTER).perform()

    def go_to_table(self):
        time.sleep(2)
        toc_button = self.browser.find_element(*PageLocators.TOC_BUTTON)
        toc_button.click()

    @property
    def videos(self):
        video_list = self.browser.find_elements(*PageLocators.VID_LOCATOR)
        print(len(video_list))
        results = [(video.get_attribute('text'), video.get_attribute('href')) for video in video_list]
        return results

    def click_pause(self):
        play_window = self.browser.find_element(*PageLocators.PLAY_WINDOW)
        play_window.click()

    def click_accept_cookies(self):
        play_window = self.browser.find_element(*PageLocators.ACCEPT_COOKIES)
        play_window.click()

    def initiate_download(self):
        try:
            initiate_button = self.browser.find_element(*PageLocators.DOWN_INITIATE1080)
        except:
            try:
                initiate_button = self.browser.find_element(*PageLocators.DOWN_INITIATE720)
            except:
                initiate_button = self.browser.find_element(*PageLocators.DOWN_INITIATE540)
        initiate_button.click()

    def complete_download(self):
        complete_button = self.browser.find_element(*PageLocators.COMPLETE_BUTTON)
        complete_button.click()
        pass

    def download_video(self):
        self.click_pause()
        time.sleep(random.randint(2, 4))
        self.initiate_download()
        WebDriverWait(self.browser, 40).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="download-img"]')
            )
        )
        time.sleep(random.randint(1, 2))
        self.complete_download()
        time.sleep(random.randint(2, 5))