from time import sleep
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions

options = ChromeOptions()

options.binary_location = r"chrome-win64\chrome.exe"
options.add_argument(r"--load-extension=adblock")
options.add_argument('--disable-notifications')
options.add_experimental_option(
    "prefs", {
        "profile.default_content_setting_values.notifications": 2
    }
)


class Main:
    def __init__(self):
        self.driver = uc.Chrome(options=options)

        while len(self.driver.window_handles) < 2:
            sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://zefoy.com")
        sleep(10)


Main()
