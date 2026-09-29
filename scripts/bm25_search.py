from pathlib import Path
import json
import jieba
from rank_bm25 import BM25Okapi

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
CHUNK_SIZE = 800
OVERLAP = 120

def split_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    text = (text or "").strip()
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

records = []
for path in sorted(PROCESSED_DIR.glob("*.jsonl")):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            content = "\n".join(x for x in [obj.get("text", ""), obj.get("tables_markdown", "")] if x)
            prefix = f"公司：{obj['company']}\n章节：{obj['section']}\n页码：{obj['page']}\n"
            for i, chunk in enumerate(split_text(content), start=1):
                records.append({
                    "company": obj["company"],
                    "section": obj["section"],
                    "page": obj["page"],
                    "chunk_no": i,
                    "text": prefix + chunk,
                })

if not records:
    raise SystemExit("没有处理后的数据。请先运行 scripts/extract_reports.py")

tokenized = [list(jieba.cut(r["text"])) for r in records]
bm25 = BM25Okapi(tokenized)

print(f"BM25索引已建立，共 {len(records)} 个块。输入问题，输入 exit 退出。")
while True:
    q = input("\n问题> ").strip()
    if not q:
        continue
    if q.lower() in {"exit", "quit"}:
        break
    scores = bm25.get_scores(list(jieba.cut(q)))
    top_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
    for rank, idx in enumerate(top_ids, start=1):
        r = records[idx]
        print(f"\n#{rank} score={scores[idx]:.3f} | {r['company']} | {r['section']} | 第{r['page']}页")
        print(r["text"][:700].replace("\n", " "))
