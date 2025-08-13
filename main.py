from seleniumbase import SB
from random import randint

from captcha_solver import CaptchaSolver

from identifiers import GeneralIdentifiers, ViewsIdentifiers, HeartsIdentifiers

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

        correct_captcha_count = 0
        incorrect_captcha_count = 0

        with SB(chromium_arg="--disable-notifications", proxy=self.proxy, uc=True, binary_location=r"chrome-win64\chrome.exe", extension_dir="adblock") as sb:
            # This is done to give the adblock extension time to install
            sb.get("https://www.webpagetest.org/blank.html")
            sb.sleep(6)
            sb.get("https://zefoy.com/")

            # Solve captcha

            if self.auto_captcha:
                self.captcha_solver.solve_captcha(sb)

            if not hearts:
                specific_identifiers = ViewsIdentifiers()
            if hearts:
                specific_identifiers = HeartsIdentifiers()

            general_identifiers = GeneralIdentifiers()

            failed = False
            try:
                sb.click(specific_identifiers.category_button)
                correct_captcha_count += 1
                print(f"Correct captcha entered | Total correct captchas: {correct_captcha_count}")

            except Exception:
                incorrect_captcha_count += 1
                print(f"Incorrect captcha entered | Total incorrect captchas: {incorrect_captcha_count}")
                failed = True
            captcha_accuracy = (correct_captcha_count / (correct_captcha_count + incorrect_captcha_count)) * 100
            print(f"Captcha accuracy so far: {captcha_accuracy}%")

            if failed:
                return

            sb.send_keys(specific_identifiers.url_input, video_url, timeout=10)

            while True:
                sb.click(specific_identifiers.search_button)
                sb.sleep(1)

                try:
                    sb.click(general_identifiers.send_button)
                    sb.sleep(1)
                    print("Completed (probably) successfully")
                    return
                except Exception:
                    sb.sleep(3)

    def change_proxy(self):

        # You will have to configure this to set self.proxy to proxies that you have access to, in the format USERNAME:PASSWORD:PROXY

        self.proxy = f""


# Set mode to 0 for views, 1 for hearts
hearts = 1

# The number of times to attempt sending views/hearts
runs = 100


def run():
    # Run 10 times
    for i in range(1, runs + 1):
        try:
            zefoy = Zefoy()
            zefoy.main()
        except Exception as err:
            print("An error occured:")
            print(err)
        print(f"Completed run {i}/{runs}")


if __name__ == "__main__":
    run()
