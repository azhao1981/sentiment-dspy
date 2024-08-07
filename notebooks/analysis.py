# -*- coding: utf-8 -*-
import os
import random
from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from typing import Any, List

load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("ZHIPUAI_API_KEY")
base_url = os.getenv("ZHIPUAI_BASE_URL")


class Analysis(BaseModel):
    messages: List[str]
    template: str = ""
    api_key: str = api_key
    base_url: str = base_url
    modelname: str = "glm-4-flash"
    template_path: str = ".\\template.txt"

    def msg2context(self):
        context = ""
        for idx, message in enumerate(self.messages):
            context += str(idx + 1) + ": " + message + "\n"
        return context

    def load_template_from_file(self):
        with open(self.template_path, "r", encoding="utf-8") as file:
            self.template = file.read()
        return self.template

    def get_response(self, prompt):
        llm = ChatOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.modelname,
            max_tokens=4095,
        )
        response = llm.invoke(prompt)
        return response

    def template2context(self):
        self.load_template_from_file()
        prompt_template = PromptTemplate(
            input_variables=["questions"], template=self.template
        )
        questions = self.msg2context()
        return prompt_template.format(questions=questions)

    def do(self):
        content = self.template2context()
        print(content)
        response = self.get_response(content)
        return response


class LangCover(BaseModel):
    en: List[Any] = []
    cn: List[Any] = []
    mapping: dict = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.mapping = self.create_mapping()

    def to_en(self, text):
        return self.mapping["cn_to_en"].get(text)

    def to_cn(self, text):
        return self.mapping["en_to_cn"].get(text, "中性")

    def create_mapping(self):
        en_to_cn = dict(zip(self.en, self.cn))
        cn_to_en = dict(zip(self.cn, self.en))
        return {"en_to_cn": en_to_cn, "cn_to_en": cn_to_en}


class Evaluate(BaseModel):
    data_set: List[Any]
    eval_set: List[Any] = []
    analyer: Analysis = None
    respone: Any = ""
    columns: List[Any] = ["label", "text", "pred_label", "main", "score"]
    random: bool = False
    modelname: str = "glm-4-flash"
    main_cover: LangCover = LangCover(
        en=["pessimistic", "optimistic", "neutral"],
        cn=["负面", "正面", "中性"],
    )
    label_cover: LangCover = LangCover(
        en=[
            "neutral",
            "surprised",
            "thankful",
            "thanking",
            "complaining",
            "urgent",
            "anxious",
            "angry",
            "happy",
        ],
        cn=["中性", "惊讶", "感激", "感激", "抱怨", "焦急", "焦急", "生气", "高兴"],
    )
    sub_cover: LangCover = LangCover(
        en=["中性", "惊讶", "感激", "抱怨", "焦急", "生气", "高兴"],
        cn=[
            "中性",
            "中性",
            "正面",
            "负面",
            "负面",
            "负面",
            "正面",
        ],
    )

    class Config:
        arbitrary_types_allowed = True

    def do(self):
        self.format_dataset()
        messages = [x.get("text") for x in self.data_set]
        self.analyer = Analysis(messages=messages, modelname=self.modelname)
        self.respone = self.analyer.do()
        return self.clear_answer()

    def is_fullcolumns(self):
        if len(self.columns) != 5:
            return False
        first_element = self.data_set[0] if self.data_set else {}
        return all(column in first_element for column in self.columns)

    def format_dataset(self):
        if self.random:
            random.shuffle(self.data_set)
        if self.is_fullcolumns():
            return
        for sample in self.data_set:
            sample["label"] = sample.get("label", "")
            sample["text"] = sample.get("text", "")
            sample["pred_label"] = ""
            sample["main"] = ""
            sample["score"] = ""

    def update_dataset(self):
        answer = self.clear_answer()
        for sample, prediction in zip(self.data_set, answer.split("\n")):
            # print(">", prediction, " ", sample)
            if prediction.strip() == "":
                continue
            result = prediction.strip().split(",")
            if len(result) != 4:
                continue
            try:
                mainCat = self.main_cover.to_cn(result[1].strip())
                label = self.label_cover.to_cn(result[2].strip())
                sample["main"] = mainCat
                sample["pred_label"] = label
                sample["score"] = result[3].strip()
            except Exception as e:
                print(e)
                print(">", prediction, " ", sample)

    def sample_error_rate(self):
        incorrect_count = sum(
            1 for sample in self.data_set if sample["pred_label"] != sample["label"]
        )
        total_count = len(self.data_set)
        return incorrect_count / total_count

    def show_error(self):
        self.update_dataset()
        print(self.sample_error_rate())
        for sample in self.data_set:
            if sample["label"] != sample["pred_label"]:
                print(sample)

    # 大类正负相反
    def is_anti_main_cat(self, label, pred_label):
        main = self.sub_cover.to_cn(label.strip())
        if main == "中性":
            return False

        sentiment_mapping = {"负面": "正面", "正面": "负面"}

        other = self.sub_cover.to_cn(pred_label.strip())
        return other == sentiment_mapping.get(main, "")

    def sample_main_error_rate(self):
        incorrect_count = sum(
            1
            for sample in self.data_set
            if self.is_anti_main_cat(sample["label"], sample["pred_label"])
        )
        total_count = len(self.data_set)
        return incorrect_count / total_count

    def show_main_error(self):
        self.update_dataset()
        print(self.sample_main_error_rate())
        for sample in self.data_set:
            if self.is_anti_main_cat(sample["label"], sample["pred_label"]):
                print(sample)

    def clear_answer(self):
        # 删除 answer 中的 'Answer: ', 删除空行
        return self.respone.content.replace("Answer:", "").strip()


if __name__ == "__main__":
    txt = """流程还没走完?
你们有真的人工服务?
比抢火车票还厉害
什么速度我靠
你们扣钱这么快吗
我觉得你挺帅
这款哈哈哈哈哈
哇,看到处理了效率真高,真好。
我非常满意
这名字怎么这么可爱
今天效率赞一个
我非常满意
买了半年没绑定手机,结果绑定以后发现唉竟然是坏的不能用
我买那么久,第一次售后就弄这一出
其它平台的认证这块太麻烦
很影响客户告知,亲爱的
都发了好几遍截图了
这件明明就是你们没检查好给我的为什么不能退?
这样谁还敢借呀
瞬间被骗了的感觉。这个皮皮网到底是个什么平台啊?
有人在么骗子公司
特么的,人死哪去了
你们就只能骗人
很好,大不了我号召我们区的玩家不玩了,本来就是一个边研发边更新的不成熟游戏,结果你们客服还那么不靠谱
如果没正常收费,我下午会打电话投诉的
办了会员不中奖这不是欺骗么
而且破损严重怎么处理?破成这样也没法送人啦"""
    analysis = Analysis(messages=txt.split("\n"))
    ret = analysis.do()
    print(ret)
