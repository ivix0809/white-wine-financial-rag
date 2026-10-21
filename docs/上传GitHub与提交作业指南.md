# 上传 GitHub 与提交作业（小白版）

## 一、先下载文件

请先下载本次提供的 `white-wine-financial-rag-final.zip`，解压后会得到 `white-wine-financial-rag-main` 文件夹。不要只把ZIP文件上传到GitHub仓库根目录；老师需要能直接浏览README、代码、测试表和截图。

## 二、推荐方法：GitHub Desktop（适合整个文件夹上传）

1. 安装 GitHub Desktop：<https://desktop.github.com/>，并登录你的GitHub账号。
2. 打开 GitHub Desktop，选择 **File → Clone repository**。
3. 选择 **URL**，输入：`https://github.com/ivix0809/white-wine-financial-rag.git`，选择本地保存位置后点 **Clone**。
4. 打开刚刚克隆的本地仓库文件夹。把解压后的 `white-wine-financial-rag-main` 文件夹里的**全部内容**复制到这个本地仓库文件夹中，并允许覆盖同名文件。
   - 复制的是里面的 `README.md`、`docs`、`tests`、`screenshots`、`scripts` 等内容，不是把外层 `white-wine-financial-rag-main` 文件夹再套一层。
   - 不要删除克隆文件夹中的隐藏 `.git` 文件夹。
   - 不要把 `.env`、API Key、密码或其他秘密信息加入仓库。
5. 回到 GitHub Desktop，确认变更列表包含新增的 `screenshots/19...` 至 `screenshots/24...`、`tests/test_results.csv`、结论和指南文件。
6. 左下方 Summary 填：`补充FastGPT混合检索实际运行证据与Q2召回记录`。
7. 点击 **Commit to main**，再点击 **Push origin**。
8. 打开网页仓库 <https://github.com/ivix0809/white-wine-financial-rag>，刷新并确认新增文件已经出现。

## 三、提交前在线检查

在GitHub网页打开并检查以下文件：

- `README.md`
- `tests/test_results.csv`
- `screenshots/19_fastgpt_hybrid_config.png`
- `screenshots/22_q2_actual_retrieval_main_data.png`
- `screenshots/24_q2_actual_answer.png`
- `docs/one_page_conclusion.md`

注意：CSV在网页上可能显示为表格或原始文本，这都正常。老师可下载查看。

## 四、作业系统里怎么填

在作业文本框中粘贴以下三行（仓库链接保持为你的真实仓库地址）：

方向：A

代码仓库：https://github.com/ivix0809/white-wine-financial-rag

一句话结论：同一批白酒半年报中，单公司单指标事实查询适合RAG，因为证据通常集中在少量财报片段并可附出处；跨公司全景分析容易漏召回，且财务口径差异和无关片段会影响答案，需要公司过滤、结构化指标及逐公司检索后汇总。

## 五、上传附件

建议按以下顺序上传：

1. `白酒财报问答知识库_一页实验结论_复核版.pdf`（一页结论，必交）。
2. `FastGPT_复核截图证据包.pdf`（将配置、Q2实际召回、实际回答截图汇总在一起，方便老师一次查看）。
3. 如果作业系统支持多张图片，再附上 `screenshots/19_fastgpt_hybrid_config.png`、`screenshots/22_q2_actual_retrieval_main_data.png` 和 `screenshots/24_q2_actual_answer.png`。若只允许一个附件，优先上传一页结论PDF，再看系统是否允许第二个附件；截图证据PDF可作为截图的汇总附件。

最后点击提交，并确认页面显示已提交/提交成功。仓库代码不需要再作为ZIP上传到作业系统，仓库链接即可；如果老师另行要求上传源码压缩包，再上传ZIP。

## 六、重要提醒

这次Q2的混合检索配置、实际召回片段和回答已有截图。其他题目仍按历史日志和原截图记录，未假称全部重新运行。Q8、Q9等失败结果保留，符合老师要求如实记录错误的要求。
