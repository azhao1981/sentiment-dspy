# -*- coding: utf-8 -*-
import os
import re
from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from typing import Any, List

load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("ZHIPUAI_API_KEY")
base_url = os.getenv("ZHIPUAI_BASE_URL")


class TransferLang(BaseModel):
    messages: List[str]
    data_set: List[Any] = []
    lang: str = "印尼语"
    template: str = "Please provide the content you want to be translated into {lang}: \n{context}\n Translation text:"
    api_key: str = api_key
    base_url: str = base_url
    modelname: str = "glm-4-flash"
    response: Any = None

    @classmethod
    def from_dataset(cls, data_set,lang="印尼语"):
        messsages = [x.get("text") for x in data_set]
        return cls(messages=messsages, lang=lang, data_set=data_set)

    def msg2context(self):
        context = ""
        for idx, message in enumerate(self.messages):
            if message.startswith("哈哈哈哈哈"):
                message = "哈哈哈哈"
            context += f"{idx+1}: " + message + "\n"
        return context

    def get_response(self, prompt):
        llm = ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.modelname,
            max_tokens=4095,
        )
        self.response = llm.invoke(
            prompt,
        )
        return self.response

    def template2context(self):
        prompt_template = PromptTemplate(
            input_variables=["context", "lang"], template=self.template
        )
        context = self.msg2context()
        return prompt_template.format(context=context, lang=self.lang)

    def do(self):
        content = self.template2context()
        print(content)
        return self.get_response(content)

    def update_set(self):
        if not self.response:
            print("No response ,run do first")
        if len(self.data_set) == 0:
            print("No data set")
        text = self.response.content.strip()
        for sample, transferred in zip(self.data_set, text.split("\n")):
            if transferred and not sample.get("source", None):
                match = re.match(r"^\d+: (.+)", transferred)
                if match:
                    source = sample.get("text")
                    sample["text"] = match.group(
                        1
                    )  # Only the part after the digit and colon
                    sample["source"] = source
