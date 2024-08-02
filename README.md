# sentiment-dspy


## 使用指南

### git

```bash
git clone ssh://git@git.flyudesk.com:9876/udesk/udesk_robot_notebooks.git
```

### dspy

```bash
# 安装 dspy
pip install dspy-ai
# or
uv pip install -r .\requrements.txt
# or
pip install -r .\requrements.txt
```

## 需求范围

### 需要支持的语言

首批支持的语言：

印尼、泰、马来、菲律宾、粤语、日语、韩语

计划支持

```
印尼语	印度尼西亚
越南语	越南
马来语	马来西亚
菲律宾	菲律宾
泰语	泰国
柬埔寨语	柬埔寨
英语	新加坡
阿拉伯	沙特阿拉伯、阿联酋、埃及
西班牙语	墨西哥
葡萄牙语	巴西
```

## 性能指标相关

[速率限制指南](https://open.bigmodel.cn/dev/howuse/rate-limits)

摘要：

并发

- 通用模型 GLM-4-Flash 5
- 通用模型 GLM-4-Flash 10

好像还有一个Token/分钟，没有找到，忘了在哪里

测试结果：

50 个需要 10s 

100 个需要 20s 输入输出 1347	1182

## 原始数据来源

```python
dict_old_cat = {"neutral":"中性", "pessimistic":"负面", "optimistic":"正面"}
dict_old_sub_cat = {"中性":"中性", "生气":"负面", "抱怨":"正面", "感激":"正面", "高兴":"正面", "惊讶":"正面", "焦急":"负面"}

["pessimistic", "optimistic", "neutral"]

情绪子分类包括 ['中性', '惊讶', '感激', '抱怨', '焦急', '生气', '高兴']
情绪子分类包括 ['neutral', 'surprised', 'thankful', 'complaining', 'anxious', 'angry', 'happy']

# liubin/tencent/tencent_get_sentiment.py
悲观的 pessimistic
乐观的 optimistic
中性 neutral

抱怨 complaining
生气 angry
高兴 happy
感激的，感谢的 thankful
var MainCat = []string{"pessimistic", "optimistic", "neutral"}
var SubCat = []string{"complaining", "angry", "happy", "thankful"}
```

## env uv + poetry

直接用 conda 加 pip 安装也可以

### 安装 uv

下载 https://github.com/astral-sh/uv/releases

```bash
which uv
```

### 安装 poetry

https://python-poetry.org/docs/ 官方的要求是建在虚拟环境中，以防止异常升级造成环境破坏。

```bash
# 修改 .env
cp .env.example .env
..\py-venv\qa\Scripts\activate.ps1

# 初始化环境和安装 poetry
build.sh
# 载入环境
. .env
# 验证
which poetry

# 添加依赖:
poetry lock
poetry install --no-root

# 运行
poetry run python main.py
```

## ref

[创建自己的数据集](https://huggingface.co/learn/nlp-course/zh-CN/chapter5/5)