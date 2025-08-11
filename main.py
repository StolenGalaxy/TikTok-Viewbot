from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from seleniumbase import SB

from PIL import Image
import os

from captcha_solver import CaptchaSolver

from random import randint

# Set the url to your TikTok video here
video_url = ""


class Zefoy(CaptchaSolver):
    def __init__(self, auto_captcha: bool = False, use_proxy: bool = False):
        self.auto_captcha = auto_captcha
        super().__init__()

        self.proxy = None
        if use_proxy:
            self.change_proxy()

        with SB(chromium_arg="--disable-notifications", proxy=self.proxy, uc=True, binary_location=r"chrome-win64\chrome.exe", extension_dir="adblock") as sb:
            # This is done to give the adblock extension time to install
            sb.get("https://google.com")
            sb.sleep(3)
            sb.get("https://zefoy.com/")

            # Solve captcha

            if auto_captcha:
                captcha = WebDriverWait(sb, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "img-thumbnail.card-img-top.border-0")))
                print("Attempting to solve captcha")
                captcha.screenshot("temp_image.png")
                image = Image.open("temp_image.png")
                image_cropped = image.crop((0, 54, image.width, 107))
                image_cropped.save("temp_image.png")
                answer = self.solve_captcha("temp_image.png")
                os.remove("temp_image.png")
                print("Entering captcha:", answer)

                sb.send_keys("#captchatoken", answer)

                sb.click(".submit-captcha")

            sb.click(".t-views-button", timeout=30)
            sb.send_keys("/html/body/div[10]/div/form/div/input", video_url, timeout=10)
            while True:
                sb.click("/html/body/div[10]/div/form/div/div/button")
                try:
                    sb.click(".wbutton.btn.btn-dark.rounded-0.font-weight-bold.p-2")
                except Exception:
                    sb.sleep(3)

    def change_proxy(self):

        # You will have to configure this to set self.proxy to a proxy that you have access to, in the format USERNAME:PASSWORD:PROXY

        self.proxy = f""


Zefoy(auto_captcha=True, use_proxy=True)
