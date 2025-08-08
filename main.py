from time import sleep
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from PIL import Image

from captcha_solver import CaptchaSolver

import os

options = ChromeOptions()

options.binary_location = r"chrome-win64\chrome.exe"
options.add_argument("--load-extension=adblock")
options.add_argument('--disable-notifications')
options.add_experimental_option(
    "prefs", {
        "profile.default_content_setting_values.notifications": 2
    }
)

video_url = "PUT THE TIKTOK VIDEO URL HERE"


class Main(CaptchaSolver):
    def __init__(self):
        super().__init__()
        self.driver = uc.Chrome(options=options)
        self.driver.get("https://google.com")
        sleep(3)
        self.driver.get("https://zefoy.com/")

        # Solve captcha
        captcha = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "img-thumbnail.card-img-top.border-0")))
        captcha.screenshot("temp_image.png")
        image = Image.open("temp_image.png")
        image_cropped = image.crop((0, 54, image.width, 107))
        image_cropped.save("temp_image.png")
        answer = self.solve_captcha("temp_image.png")
        os.remove("temp_image.png")
        print("Entering captcha:", answer)
        captcha_box = self.driver.find_element(By.ID, "captchatoken")
        captcha_box.send_keys(answer)
        self.driver.find_element(By.CLASS_NAME, "submit-captcha").click()

        sleep(2)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "t-views-button"))).click()
        sleep(2)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[10]/div/form/div/input"))).send_keys(video_url)
        sleep(2)
        while True:
            self.driver.find_element(By.XPATH, "/html/body/div[10]/div/form/div/div/button").click()
            sleep(3)
            try:
                self.driver.find_element(By.CLASS_NAME, "wbutton.btn.btn-dark.rounded-0.font-weight-bold.p-2").click()
            except Exception:
                sleep(3)


Main()
