How to use

1. Download the current beta version of chrome for win64 here: https://googlechromelabs.github.io/chrome-for-testing/
(The program will not work if you use the stable version due to extension loading being disabled in stable chrome)

2. Extract the zip file and place the folder called "chrome-win64" into the same location as main.py

If you want the captchas to be solved automatically:
    1. Rename .env.template to .env and enter your OpenAI Api Key
    2. Run Zefoy() with auto_captcha = True
    It usually costs about $0.01 per captcha

If you want to use proxies to bypass the wait time:
    1. You will have to edit the change_proxy() function to set self.proxy to one of your proxies
    2. Run Zefoy() with use_proxy = True
