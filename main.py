from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import sys

identifiers = {
    "views": "btn.btn-primary.rounded-0.t-views-button",
    "urlBox": '//div[@class="col-sm-5 col-xs-12 p-1 container t-views-menu"]//input[@placeholder]',
    "urlButton": '//div[@class="col-sm-5 col-xs-12 p-1 container t-views-menu"]//button',
    "submitButton": '//div[@class="col-sm-5 col-xs-12 p-1 container t-views-menu"]//button[contains(@class, "wbutton")]'
}


class Zefoy:
    def __init__(self, videoURL):
        self.url = videoURL
        self.driver = webdriver.Chrome()

    def main(self):
        self.driver.get("https://zefoy.com/")

        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, identifiers["views"])))
        self.driver.find_element(By.CLASS_NAME, identifiers["views"]).click()

        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, identifiers["urlBox"])))
        self.driver.find_element(By.XPATH, identifiers["urlBox"]).send_keys(self.url)

        self.driver.find_element(By.XPATH, identifiers["urlButton"]).click()

        while True:
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, identifiers["submitButton"])))
                sleep(1)
                self.driver.find_element(By.XPATH, identifiers["submitButton"]).click()
            except:
                self.driver.find_element(By.XPATH, identifiers["urlButton"]).click()
                    




Zefoy("https://www.tiktok.com/@meepkid69/video/7048179708994800901").main()
