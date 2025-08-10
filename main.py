from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from seleniumbase import SB

from PIL import Image

from captcha_solver import CaptchaSolver


import os

proxy_1 = ""

video_url = ""


class Main(CaptchaSolver):
    def __init__(self, auto_captcha: bool = True, proxy: str = ""):
        self.auto_captcha = auto_captcha
        super().__init__()

        with SB(chromium_arg="--disable-notifications", proxy=proxy_1, uc=True, ad_block_on=True) as sb:
            sb.get("https://google.com")
            sleep(3)
            sb.get("https://zefoy.com/")
            sleep(3)

            # Solve captcha
            captcha = WebDriverWait(sb, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "img-thumbnail.card-img-top.border-0")))
            captcha.screenshot("temp_image.png")
            image = Image.open("temp_image.png")
            image_cropped = image.crop((0, 54, image.width, 107))
            image_cropped.save("temp_image.png")
            answer = self.solve_captcha("temp_image.png")
            os.remove("temp_image.png")
            print("Entering captcha:", answer)
            captcha_box = sb.find_element(By.ID, "captchatoken")
            captcha_box.send_keys(answer)
            sb.find_element(By.CLASS_NAME, "submit-captcha").click()

            sleep(2)
            WebDriverWait(sb, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "t-views-button"))).click()
            sleep(2)
            WebDriverWait(sb, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[10]/div/form/div/input"))).send_keys(video_url)
            sleep(2)
            while True:
                sb.find_element(By.XPATH, "/html/body/div[10]/div/form/div/div/button").click()
                sleep(3)
                try:
                    sb.find_element(By.CLASS_NAME, "wbutton.btn.btn-dark.rounded-0.font-weight-bold.p-2").click()
                except Exception:
                    sleep(3)


Main()
