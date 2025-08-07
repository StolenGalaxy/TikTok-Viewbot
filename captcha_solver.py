from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv


class ResponseFormat(BaseModel):
    word: str


class CaptchaSolver:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def create_file(self, path):
        with open(path, "rb") as file_content:
            result = self.client.files.create(
                file=file_content,
                purpose="vision",
            )
            return result.id

    def solve_captcha(self, path):
        response = self.client.responses.parse(
            model="o3",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Provide the EXACT WORD spelt out from left to right in the provided image"
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
