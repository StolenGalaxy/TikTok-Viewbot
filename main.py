from seleniumbase import SB
from random import randint

from captcha_solver import CaptchaSolver

# Set the url to your TikTok video here
video_url = ""


class Zefoy():
    def __init__(self, auto_captcha: bool = True, use_proxy: bool = True):
        self.auto_captcha = auto_captcha
        self.proxy = None
        self.captcha_solver = CaptchaSolver()
        if use_proxy:
            self.change_proxy()

    def main(self):
        with SB(chromium_arg="--disable-notifications", proxy=self.proxy, uc=True, binary_location=r"chrome-win64\chrome.exe", extension_dir="adblock") as sb:
            # This is done to give the adblock extension time to install
            sb.get("https://google.com")
            sb.sleep(3)
            sb.get("https://zefoy.com/")

            # Solve captcha

            if self.auto_captcha:
                self.captcha_solver.solve_captcha(sb)

            if not hearts:
                sb.click(".t-views-button", timeout=30)
                sb.send_keys("/html/body/div[10]/div/form/div/input", video_url, timeout=10)
                while True:
                    sb.click("/html/body/div[10]/div/form/div/div/button")
                    sb.sleep(1)
                    try:
                        sb.click(".wbutton.btn.btn-dark.rounded-0.font-weight-bold.p-2")
                        print("Successfully sent views!")
                        return
                    except Exception:
                        sb.sleep(3)

            if hearts:
                sb.click(".t-hearts-button", timeout=30)
                sb.send_keys("/html/body/div[8]/div/form/div/input", video_url, timeout=10)
                while True:
                    sb.click("/html/body/div[8]/div/form/div/div/button")
                    sb.sleep(1)
                    try:
                        sb.click(".wbutton.btn.btn-dark.rounded-0.font-weight-bold.p-2")
                        print("Successfully sent hearts!")
                        return
                    except Exception:
                        sb.sleep(3)

    def change_proxy(self):

        # You will have to configure this to set self.proxy to proxies that you have access to, in the format USERNAME:PASSWORD:PROXY

        self.proxy = f""


# Set mode to 0 for views, 1 for hearts
hearts = 1


def run():
    # Run 10 times
    for i in range(10):
        try:
            zefoy = Zefoy()
            zefoy.main()
        except Exception as err:
            print("An error occured:")
            print(err)


if __name__ == "__main__":
    run()
