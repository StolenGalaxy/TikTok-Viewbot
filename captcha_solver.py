from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

import cv2


class ResponseFormat(BaseModel):
    word: str


class CaptchaSolver:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def create_file(self, path) -> str:
        with open(path, "rb") as file_content:
            result = self.client.files.create(
                file=file_content,
                purpose="vision",
            )
            return result.id

    def solve_captcha(self, path) -> str:
        self.remove_lines(path)
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
                            "file_id": self.create_file(path),
                        },
                        ],
                }
            ],
            text_format=ResponseFormat
        )
        response = response.to_dict()
        print(response)
        answer = response["output"][1]["content"][0]["parsed"]["word"]
        return answer

    def remove_lines(self, path):
        # ChatGPT wrote this to remove the black lines in the captchas
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

        detected_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        result = cv2.inpaint(img, detected_lines, 3, cv2.INPAINT_TELEA)

        cv2.imwrite(path, result)
