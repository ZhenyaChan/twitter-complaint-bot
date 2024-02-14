from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import credentials

# change your internet speed and provider name
TEST_TIME = 45
PROMISED_DOWN = 500
PROMISED_UP = 200
PROVIDER = "Rogers"
SPEED_TEST_SITE = "https://www.speedtest.net/"
TWITTER_SITE = "https://twitter.com/"
LOGIN = credentials.TWITTER_LOGIN
PASS = credentials.TWITTER_PASSWORD


class Twitter_Complaint_Bot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        ser = Service(executable_path="/Users/dung/chromedriver")
        self.driver = webdriver.Chrome(options=chrome_options, service=ser)
        self.down = 0
        self.up = 0

    def get_internet_speed(self, site_name):
        self.driver.get(site_name)
        # start measuring internet speed
        start_button = self.driver.find_element(By.CLASS_NAME, value="start-button")
        start_button.click()
        time.sleep(TEST_TIME)
        # close the pop-up window
        close_button = self.driver.find_element(By.XPATH, value="//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/p[2]/button")
        close_button.click()
        time.sleep(2)

        download_speed = self.driver.find_element(By.CSS_SELECTOR, value=".download-speed")
        print("Download speed: ", download_speed.text)
        self.down = float(download_speed.text)

        upload_speed = self.driver.find_element(By.CSS_SELECTOR, value=".upload-speed")
        print("Upload speed: ", upload_speed.text)
        self.up = float(upload_speed.text)

    def tweet(self, site_name, msg):
        # login into twitter
        self.driver.get(site_name)
        time.sleep(3)
        sign_in_btn = self.driver.find_element(By.XPATH, value="//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div")
        sign_in_btn.click()
        time.sleep(3)

        # entering credentials
        input_fld = self.driver.find_element(By.NAME, value="text")
        input_fld.send_keys(LOGIN)
        time.sleep(1)
        next_btns = self.driver.find_elements(By.CSS_SELECTOR, value='div[role="button"]')
        for next_btn in next_btns:
            if next_btn.text == "Next":
                next_btn.click()
                break

        time.sleep(5)
        input_fld = self.driver.find_element(By.NAME, value="password")
        input_fld.send_keys(PASS)

        log_in_btns = self.driver.find_elements(By.CSS_SELECTOR, value='div[role="button"]')
        for log_in_btn in log_in_btns:
            if log_in_btn.text == "Log in":
                log_in_btn.click()
                break

        time.sleep(5)

        # write a complaint message
        input_fld = self.driver.find_element(By.CSS_SELECTOR, value='[data-contents="true"]')
        input_fld.send_keys(msg)
        time.sleep(1)

        # post a complaint message
        post_btns = self.driver.find_elements(By.CSS_SELECTOR, value='div[role="button"]')
        for post_btn in post_btns:
            if post_btn.text == "Post":
                post_btn.click()
                break

        # self.driver.quit()


# create bot object and call speed and tweet functions
twitter_complaint_bot = Twitter_Complaint_Bot()
twitter_complaint_bot.get_internet_speed(SPEED_TEST_SITE)
twitter_complaint_bot.tweet(TWITTER_SITE, f"Hey {PROVIDER}, why is my internet speed {twitter_complaint_bot.down} down/"
                                          f"{twitter_complaint_bot.up} up, when I pay for {PROMISED_DOWN} down/{PROMISED_UP} up?")
