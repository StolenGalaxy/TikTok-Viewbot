from time import sleep
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from PIL import Image

from captcha_solver import CaptchaSolver

options = ChromeOptions()

options.binary_location = r"chrome-win64\chrome.exe"
options.add_argument(r"--load-extension=adblock")
options.add_argument('--disable-notifications')
options.add_experimental_option(
    "prefs", {
        "profile.default_content_setting_values.notifications": 2
    }
)


class Main(CaptchaSolver):
    def __init__(self):
        super().__init__()
        self.driver = uc.Chrome(options=options)

        while len(self.driver.window_handles) < 2:
            sleep(0.5)

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://zefoy.com")

        captcha = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "img-thumbnail.card-img-top.border-0")))
        captcha.screenshot("testimage.png")
        image = Image.open("testimage.png")
        image_cropped = image.crop((0, 54, image.width, 107))
        image_cropped.save("testimage.png")
        answer = self.solve_captcha("testimage.png")
        print(answer)


Main()
