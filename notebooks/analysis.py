import os
from dotenv import find_dotenv, load_dotenv
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("ZHIPUAI_API_KEY")
model_name = "glm-4-flash"


class Analysis(BaseModel):
    messages: list[str]
    template: str = ""
    api_key: str = "29cf286465d10e939d3ec7c4786ab076.7OCmqNDeGcyE9pn8"
    base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    model_name: str = "glm-4-flash"
    template_path: str = ".\\template.txt"

    def msg2context(self):
        context = ""
        for idx, message in enumerate(self.messages):
            context += str(idx) + ": " + message + "\n"
        return context

    def load_template_from_file(self):
        with open(self.template_path, "r", encoding="utf-8") as file:
            self.template = file.read()
        return self.template

    def get_response(self, prompt):
        llm = ChatOpenAI(
            api_key=self.api_key, base_url=self.base_url, model=self.model_name
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
