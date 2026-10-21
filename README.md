# 白酒行业2026年半年报问答知识库

## 项目简介

本项目选取10家白酒上市公司2026年半年度报告，使用 FastGPT
构建财报RAG问答知识库。

主要流程： 1. 从交易所网站下载半年报全文； 2. 将PDF导入知识库并切块； 3.
使用向量检索 + 全文/BM25式检索的混合检索； 4.
使用重排模型优化候选块排序； 5. 创建对话Agent，回答问题并显示来源； 6.
设计10道测试题（含2道跨公司全景题），记录召回内容、正确性和错误原因。

> 主问答页面由 FastGPT 完成。本仓库中的 Python
> 脚本用于本地抽取、页码/章节标记和 BM25 检索演示，便于复现和说明方法。

## 10家公司

-   600519 贵州茅台
-   600809 山西汾酒
-   600702 舍得酒业
-   600779 水井坊
-   600559 老白干酒
-   603369 今世缘
-   603198 迎驾贡酒
-   603589 口子窖
-   603919 金徽酒
-   600197 伊力特

## FastGPT主要配置

-   文档处理：分块存储
-   分块阈值：原文长度大于1000
-   标题加入索引：开启
-   搜索方式：混合检索
-   语义检索权重：0.3
-   全文检索权重：0.7
-   结果重排：开启
-   重排模型：gte-rerank-v2

## 向量检索实现说明

本项目的实际问答系统由 FastGPT 完成。

向量检索部分：
- Embedding模型：阿里 emb3
- 检索方式：混合检索
- 语义检索权重：0.3
- 全文检索权重：0.7
- 重排模型：gte-rerank-v2

仓库中的 Python 脚本主要用于：
- 财报下载
- PDF解析
- 页码和章节信息保留
- BM25检索复现实验

因此实际系统流程为：

PDF财报
→ FastGPT知识库切块
→ 向量检索 + 全文检索
→ 重排
→ 生成带出处回答

## 本地运行（可选）

将10份PDF放到 `data/pdfs/`。

``` bash
pip install -r requirements.txt
python scripts/extract_reports.py
python scripts/bm25_search.py
```

## 文件结构

``` text
white_wine_financial_rag_homework/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ scripts/
│  ├─ extract_reports.py
│  ├─ bm25_search.py
│  └─ download_reports.py
├─ data/
│  ├─ company_list.csv
│  ├─ report_urls.csv
│  ├─ pdfs/
│  └─ processed/
├─ tests/
│  ├─ questions.csv
│  └─ test_results.csv
├─ docs/
│  ├─ one_page_conclusion.md
│  └─ fastgpt_config.md
└─ screenshots/
   └─ README.txt
```

## 已观察到的典型现象

-   单公司、单指标问题通常表现较好。
-   财报中"营业收入/营业总收入""合并/母公司"口径相近时，可能出现错误召回。
-   跨10家公司进行全景比较时，普通分块RAG容易只召回少数公司。
-   多轮对话中可能出现上一题公司的内容串入下一题，需要通过问题优化、明确公司过滤或重开会话降低影响。

## 测试记录

共设计10道测试问题，其中： - 8道单公司事实查询； -
2道跨公司全景分析问题。

测试记录包含： - 用户问题； - 召回结果； - 是否回答正确； -
错误原因分析。

典型测试结果：

  类型               效果   说明
  ------------------ ------ ------------------------------------
  单公司单指标查询   较好   答案通常可以从对应财报片段中召回
  财务口径判断问题   一般   营业收入、营业总收入等指标容易混淆
  跨公司比较问题     较弱   多家公司信息同时召回时容易漏召回
  多轮连续问答       一般   公司切换时可能产生上下文串扰

## 实验结论

同一批财报材料中，不同问题适合不同方法：

-   单公司、单指标事实查询适合 RAG，因为答案通常集中在少量财报片段中；
-   跨公司全景分析更容易受到召回范围限制，需要增加公司过滤、结构化指标提取和多轮检索；
-   财报问答的主要难点不是生成，而是正确理解财务口径并召回正确来源。

## 后续优化方向

1.  增加公司名称过滤，避免不同公司的财报内容混淆；
2.  对营业收入、净利润等核心指标建立结构化字段；
3.  对跨公司问题采用分公司检索后再汇总的方法；
4.  优化切块策略，使表格信息和页码信息保留更加完整。

## 本次复核补充：实际运行证据

- `screenshots/18_fastgpt_knowledge_base_index_model.png`：知识库包含10份报告，索引模型显示为阿里-emb3。
- `screenshots/19_fastgpt_hybrid_config.png` 和 `screenshots/19b_fastgpt_search_filter_config.png`：实际界面显示混合检索语义权重0.3、全文权重0.7，结果重排开启，模型为 `gte-rerank-v2`，并记录引用上限/最低相关度。
- `screenshots/20_q2_runtime_search_parameters.png` 和 `screenshots/21_q2_runtime_embedding_rerank.png`：Q2本次完整响应显示实际问题、混合检索参数、阿里-emb3、gte-rerank-v2及重排权重。
- `screenshots/22_q2_actual_retrieval_main_data.png`、`screenshots/23_q2_actual_retrieval_source_footer_and_other_result.png`、`screenshots/24_q2_actual_answer.png`：展示Q2实际召回表格、结果卡片文件名上下文、以及带第4页出处的实际回答。召回响应同时包含不相关片段，已如实记录为检索噪声。
- `tests/test_results.csv`：保留原10题评价和失败分析，增加每题实际输出证据、检索方式的证据级别和复核备注。Q2为本次实际复测；其他题目使用历史日志/原截图，不冒充本次重新运行。
- `tests/dialogue_log_evidence.csv` 与 `docs/对话日志证据整理说明.md`：整理历史对话输出、引用ID、可见页码及其限制，不包含不必要的用户标识/IP/`reasoning`字段。
- `docs/one_page_conclusion.md` 和 `白酒财报问答知识库_一页实验结论_复核版.pdf`：更新后的实验结论。
- `docs/上传GitHub与提交作业指南.md`：GitHub上传及作业提交步骤。

### 证据边界

FastGPT当前混合检索配置和Q2本次运行已有截图。历史日志没有为每道题保存单轮完整检索参数，因此其他题的历史检索模式不能仅凭日志独立复原；原有正确、部分正确、错误评价及错因均保留。
