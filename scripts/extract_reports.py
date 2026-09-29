from pathlib import Path
import json
import re
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "data" / "pdfs"
OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SECTION_RE = re.compile(r"(第[一二三四五六七八九十百0-9]+节[^\n]*)")

def company_from_filename(name: str) -> str:
    stem = Path(name).stem
    parts = stem.split("_")
    return parts[1] if len(parts) >= 2 else stem

def markdown_table(table):
    if not table:
        return ""
    width = max(len(r or []) for r in table)
    cleaned = []
    for row in table:
        row = row or []
        vals = [(c or "").replace("\n", " ").strip() for c in row]
        vals += [""] * (width - len(vals))
        cleaned.append(vals)
    if not cleaned:
        return ""
    rows = ["| " + " | ".join(cleaned[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for row in cleaned[1:]:
        rows.append("| " + " | ".join(row) + " |")
    return "\n".join(rows)

for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
    company = company_from_filename(pdf_path.name)
    out_path = OUT_DIR / f"{pdf_path.stem}.jsonl"
    current_section = "未识别章节"

    with pdfplumber.open(pdf_path) as pdf, out_path.open("w", encoding="utf-8") as f:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            m = SECTION_RE.search(text)
            if m:
                current_section = m.group(1).strip()

            tables_md = []
            try:
                for table in page.extract_tables() or []:
                    md = markdown_table(table)
                    if md:
                        tables_md.append(md)
            except Exception:
                pass

            record = {
                "company": company,
                "file": pdf_path.name,
                "page": page_no,
                "section": current_section,
                "text": text,
                "tables_markdown": "\n\n".join(tables_md),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"完成: {pdf_path.name} -> {out_path.name}")
