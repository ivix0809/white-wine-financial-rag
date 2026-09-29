from pathlib import Path
import csv
import requests

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "report_urls.csv"
OUT_DIR = ROOT / "data" / "pdfs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with CSV_PATH.open("r", encoding="utf-8-sig") as f:
    rows = csv.DictReader(f)
    for row in rows:
        url = (row.get("url") or "").strip()
        filename = (row.get("filename") or "").strip()
        if not url or not filename:
            continue
        print(f"下载: {filename}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        (OUT_DIR / filename).write_bytes(r.content)
        print("完成")
