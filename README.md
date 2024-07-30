# sentiment-dspy

## dspy

```bash
pip install dspy-ai
uv pip install -r .\requrements.txt
```

## 性能

## 需要支持的语言

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

## start


[创建自己的数据集](https://huggingface.co/learn/nlp-course/zh-CN/chapter5/5)

## 性能

https://open.bigmodel.cn/dev/howuse/rate-limits

并发
通用模型 GLM-4-Flash 5
通用模型 GLM-4-Flash 10

好像还有一个Token/分钟

100 个需要20s
输入输出
1347	1182
## env

uv + poetry

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

### 项目结构:
```
my_project/
├── poetry.toml
├── pyproject.toml
└── main.py
```
