# 白酒行业2026年半年报问答知识库

## 项目简介
本项目选取10家白酒上市公司2026年半年度报告，使用 FastGPT 构建财报RAG问答知识库。

主要流程：
1. 从交易所网站下载半年报全文；
2. 将PDF导入知识库并切块；
3. 使用向量检索 + 全文/BM25式检索的混合检索；
4. 使用重排模型优化候选块排序；
5. 创建对话Agent，回答问题并显示来源；
6. 设计10道测试题（含2道跨公司全景题），记录召回内容、正确性和错误原因。

> 主问答页面由 FastGPT 完成。本仓库中的 Python 脚本用于本地抽取、页码/章节标记和 BM25 检索演示，便于复现和说明方法。

## 10家公司
- 600519 贵州茅台
- 600809 山西汾酒
- 600702 舍得酒业
- 600779 水井坊
- 600559 老白干酒
- 603369 今世缘
- 603198 迎驾贡酒
- 603589 口子窖
- 603919 金徽酒
- 600197 伊力特

## FastGPT主要配置
- 文档处理：分块存储
- 分块阈值：原文长度大于1000
- 标题加入索引：开启
- 搜索方式：混合检索
- 语义检索权重：0.3
- 全文检索权重：0.7
- 结果重排：开启
- 重排模型：gte-rerank-v2

## 本地运行（可选）
将10份PDF放到 `data/pdfs/`。

```bash
pip install -r requirements.txt
python scripts/extract_reports.py
python scripts/bm25_search.py
```

## 文件结构
```text
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
- 单公司、单指标问题通常表现较好。
- 财报中“营业收入/营业总收入”“合并/母公司”口径相近时，可能出现错误召回。
- 跨10家公司进行全景比较时，普通分块RAG容易只召回少数公司。
- 多轮对话中可能出现上一题公司的内容串入下一题，需要通过问题优化、明确公司过滤或重开会话降低影响。
