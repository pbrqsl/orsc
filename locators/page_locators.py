from selenium.webdriver.common.by import By

class PageLocators:
    EMAIL_ADDRESS_INPUT = By.XPATH, '//input[@type="email"]'
    TOC_BUTTON = By.XPATH, '//button[@title="Table of Contents"]'
    VID_LOCATOR = By.XPATH, '//li/section/article/h6/a'
    COURSE_TITLE = By.XPATH, '//h3/a'
    PLAY_BUTTON = By.XPATH, '//button[@aria-label="Play"]'
    PLAY_WINDOW = By.XPATH, '//iframe[@allow="fullscreen *;"]'
    DOWN_INITIATE1080 = By.XPATH, '//div[contains(@class, "resImg resImg1080p")]'
    DOWN_INITIATE720 = By.XPATH, '//div[contains(@class, "resImg resImg720p")]'
    DOWN_INITIATE540 = By.XPATH, '//div[contains(@class, "resImg resImg540p")]'
    COMPLETE_BUTTON = By.XPATH, '//div[@class="download-img"]'
    ACCEPT_COOKIES = By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'
