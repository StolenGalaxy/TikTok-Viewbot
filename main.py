from seleniumbase import SB

from captcha_solver import CaptchaSolver
from identifiers import GeneralIdentifiers, ViewsIdentifiers, HeartsIdentifiers

# Set the url to your TikTok video here
video_url = ""


class Zefoy():
    def __init__(self, auto_captcha: bool = True, use_proxy: bool = True):
        self.auto_captcha = auto_captcha
        self.use_proxy = use_proxy
        self.proxy = None
        self.captcha_solver = CaptchaSolver()

        self.correct_captcha_count = 0
        self.incorrect_captcha_count = 0

        self.attribute_count = 0

    def main(self):
        if self.use_proxy:
            self.change_proxy()

        with SB(chromium_arg="--disable-notifications", proxy=self.proxy, uc=True, binary_location=r"chrome-win64\chrome.exe", extension_dir="adblock") as sb:
            # This is done to give the adblock extension time to install
            sb.get("https://www.webpagetest.org/blank.html")
            sb.sleep(6)
            sb.get("https://zefoy.com/")

            # Solve captcha

            if not hearts:
                specific_identifiers = ViewsIdentifiers()
            if hearts:
                specific_identifiers = HeartsIdentifiers()

            general_identifiers = GeneralIdentifiers()

            failed = False
            try:
                if self.auto_captcha:
                    self.captcha_solver.solve_captcha(sb)

                sb.click(specific_identifiers.category_button)
                self.correct_captcha_count += 1

                captcha_accuracy = (self.correct_captcha_count / (self.correct_captcha_count + self.incorrect_captcha_count)) * 100
                print(f"Correct captcha entered | Total correct captchas: {self.correct_captcha_count} | Captcha accuracy: {captcha_accuracy}%")

            except Exception:
                self.incorrect_captcha_count += 1

                captcha_accuracy = (self.correct_captcha_count / (self.correct_captcha_count + self.incorrect_captcha_count)) * 100
                print(f"Incorrect captcha entered | Total incorrect captchas: {self.incorrect_captcha_count} | Captcha accuracy: {captcha_accuracy}%")
                failed = True

            if failed:
                return

            sb.send_keys(specific_identifiers.url_input, video_url, timeout=10)

            search_count = 0
            while True:
                sb.click(specific_identifiers.search_button)
                sb.sleep(10)

                search_count += 1
                if sb.is_element_visible(general_identifiers.send_button):
                    sb.sleep(1)
                    self.attribute_count = sb.find_element(general_identifiers.send_button).text

                    print(f"Current view/heart count: {self.attribute_count}")
                    sb.click(general_identifiers.send_button)
                    sb.sleep(3)
                    return
                elif search_count > 75:
                    print("Run appears to have gotten trapped. Restarting.")
                    return

    def change_proxy(self):

        # You will have to configure this to set self.proxy to proxies that you have access to, in the format USERNAME:PASSWORD:PROXY

        self.proxy = f""


def run():
    # Run 10 times
    for i in range(1, runs + 1):
        print(f"-----------------Start of run {i}/{runs}-----------------")
        try:
            zefoy.main()
        except Exception as err:
            print(f"An error occured:\n{err}")


if __name__ == "__main__":
    # Set mode to 0 for views, 1 for hearts
    hearts = 1

    # The number of times to attempt sending views/hearts
    runs = 100

    zefoy = Zefoy()
    run()
