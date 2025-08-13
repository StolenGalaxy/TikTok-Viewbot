from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from PIL import Image
import os

from identifiers import CaptchaIdentifiers


class ResponseFormat(BaseModel):
    word: str


class CaptchaSolver:
    def __init__(self):
        load_dotenv()
        self.image_path = "temp_image.png"
        self.client = OpenAI()

        self.identifiers = CaptchaIdentifiers()

    def solve_captcha(self, sb):
        self.sb = sb
        self.save_captcha()

        captcha_answer = self.get_answer()

        os.remove(self.image_path)

        print("Entering captcha:", captcha_answer)

        self.sb.send_keys(self.identifiers.captcha_input, captcha_answer)

        self.sb.click(self.identifiers.submit_button)

    def save_captcha(self):
        captcha = self.sb.find_element(self.identifiers.captcha_image)
        # captcha = WebDriverWait(self.sb, 30).until(EC.presence_of_element_located((By.CLASS_NAME, self.identifiers.captcha_image)))
        print("Attempting to solve captcha")

        captcha.screenshot(self.image_path)
        image = Image.open(self.image_path)
        image_cropped = image.crop((0, 54, image.width, 107))
        image_cropped.save(self.image_path)

    def create_file(self) -> str:
        with open(self.image_path, "rb") as file_content:
            result = self.client.files.create(
                file=file_content,
                purpose="vision",
            )
            return result.id

    def get_answer(self) -> str:
        response = self.client.responses.parse(
            model="o3",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "What word is spelt out from left to right in this image, with letters alternating between the top and bottom lines?"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "file_id": self.create_file(),
                        },
                        ],
                }
            ],
            text_format=ResponseFormat
        )
        response = response.to_dict()
        answer = response["output"][1]["content"][0]["parsed"]["word"]
        return answer
