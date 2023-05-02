import openai

from . import config

with open("./fixtures/resume.txt", mode="r", encoding="utf8") as resume_file:
    resume_content = resume_file.read()


def prepare_messages(rows):
    return list(map(lambda row: {"content": row["message"], "role": row["role"]}, rows))


class ChatApp:
    def __init__(self, settings: config.OpenAI):
        self.settings = settings 
        openai.api_key = self.settings.api_key
        self.premice = {
            "role": "system",
            "content": f"You will answer as if your were Tom DUPUY. Here is his resume: {resume_content}",
        }

    def chat(self, messages: list) -> str:
        messages = prepare_messages(messages)
        messages.insert(0, self.premice)
        response = openai.ChatCompletion.create(
            model=self.settings.chat_completion_model, messages=messages
        )
        return response["choices"][0]["message"].content
