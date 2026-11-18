# 先看这里：运行和交作业

## 已做好的部分

四个主要 Python 文件、11 条官方来源知识库、三个类别、搜索评分、分类浏览、隐私拦截、JSON 历史记录、统计指标、CSV 导出、20 项自动化测试、葡语 README、视频讲稿和提交 TXT 模板。

当前按个人作业准备，学校身份使用截图中的 YIHANG XU / RM 571720 / 1CCPY。若你实际有组员，请在 README、TXT、评论和视频中补齐所有成员。

## 1. 运行

解压 ZIP，进入 citizen-assist-ai 文件夹，在终端运行：

```bash
python main.py
```

Mac 若提示找不到 python，使用 `python3 main.py`。需要 Python 3.10 或更新版本，无需安装第三方包。不要在 ZIP 内直接运行。

菜单：1 提问；2 分类；3 统计；4 导出 CSV；5 重新加载知识库；0 退出。退出时输入 1–5 的易用性评分；评分页输入 0 是返回菜单。

先试 `Como obter carteira de trabalho digital?`，应找到工作卡说明，7 分，高匹配度。

## 2. 必须由真人完成的测试

找至少 3 个非组员，累计至少 10 次咨询；每个人单独打开程序，结束时给自己的评分。不要记录姓名或联系方式。

先用单独一份项目练习，避免练习记录混进正式用户测试。正式测试目录中的历史和评分 JSON 初始为 `[]`。详细流程见 `TESTE_COM_USUARIOS.md`。

测试结束后用选项 3 查看结果，填进 README 的 PENDENTE 表格。根据真实问题做至少一个改进，再记录改进前后结果。不要把自动化测试说成真人测试。

## 3. 录制视频

按 `ROTEIRO_VIDEO.md` 的葡语讲稿练习；总时长 5–8 分钟，目标 7 分半。

必须你本人讲代码，不能 AI 配音。可以不露脸。录清楚代码、程序运行和现场修改关键词。三个人组队就三个人都要讲技术内容。

脚本中的真人测试数据留空，需要填入真实结果。现场改词示例是演示，不能冒充用户测试观察。

视频上传 YouTube，选择 Não listado。GitHub 仓库要 Public，两者都不能要求老师额外申请权限。

## 4. GitHub 和提交

本包尚未创建远程 GitHub 仓库，也没有替你上传 YouTube 或提交 FIAP。

在 GitHub 创建公开仓库 citizen-assist-ai，把解压后文件夹里的内容上传，根目录应直接看见 README.md 和 main.py。保留 data 和 tests 文件夹。别上传整个 ZIP 代替源代码。

提交前检查历史里没有真人个人信息，不上传 .bak、临时目录或账号信息。把真人测试结果补进 README，再加入 GitHub 和 YouTube 链接。

将 `ENTREGA_PORTAL_MODELO.txt` 改名为 `ENTREGA_PORTAL.txt`，删除第一行模板警告和个人身份旁的待确认说明，填上两个真实链接。确认没有 PENDENTE 后，仅上传这个 TXT 到 FIAP 作业页面。

评论区个人提交可填写：

```text
Trabalho individual.
Integrante: YIHANG XU — RM 571720.
```

截图截止为 2026 年 11 月 19 日 23:55；PDF 写 23:59。按更早的 23:55 完成。

## 5. 录视频前要懂的代码

| 技术词 | 中文解释 |
|---|---|
| classe / objeto | 类是结构，对象是创建出的实例 |
| atributo / método | 属性存数据，方法执行功能 |
| self | 当前对象本身 |
| composição | Assistente 拥有 BaseConhecimento，后者拥有多个 Orientacao |
| dicionário | JSON 一条记录读进 Python 后的键值结构 |
| tupla | 搜索返回的 (分数, 指导对象) |
| normalizar | 去重音、去标点、转小写，统一比较格式 |
| pontuar | 关键词 +3，标题符合条件的单词 +1 |
| CSV | 有表头的表格文本，用 DictWriter 导出 |

程序不是连着 ChatGPT 的聊天机器人。老师要求的“智能”主要是解释得清楚的规则搜索。不要只背稿，要能指出每个功能对应的代码。
