# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
"""
Rebuild reports.json by scanning projects/*/*.html
Usage:
    python tools/build_reports_json.py
"""
import os, json, re, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(ROOT, "projects")
OUT = os.path.join(ROOT, "reports.json")

def extract_meta(html_text):
    meta = {"title": "", "ts": ""}
    m = re.search(r'class="hero-title"[^>]*>(.*?)</', html_text, re.DOTALL | re.IGNORECASE)
    if m:
        meta["title"] = re.sub(r"\s+", " ", m.group(1)).strip()
    m2 = re.search(r'class="ts"[^>]*>(.*?)</', html_text, re.DOTALL | re.IGNORECASE)
    if m2:
        meta["ts"] = re.sub(r"\s+", " ", m2.group(1)).strip()
    else:
        m3 = re.search(r'Сформировано:([^<\n\r]+)', html_text, re.IGNORECASE)
        if m3:
            meta["ts"] = "Сформировано:" + re.sub(r"\s+", " ", m3.group(1)).strip()
    return meta

def guess_code_and_name(proj_id):
    parts = proj_id.split("_", 1)
    code = parts[0] if parts else proj_id
    name = parts[1] if len(parts) > 1 else proj_id
    return code, name

def write_json_utf8(obj, path):
    data = json.dumps(obj, ensure_ascii=False, indent=2)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(data)

def main():
    items = []
    if not os.path.isdir(PROJECTS_DIR):
        print("No 'projects' dir found: {}".format(PROJECTS_DIR))
        return
    for proj_id in sorted(os.listdir(PROJECTS_DIR)):
        pdir = os.path.join(PROJECTS_DIR, proj_id)
        if not os.path.isdir(pdir):
            continue
        code, name = guess_code_and_name(proj_id)
        htmls = [f for f in os.listdir(pdir) if f.lower().endswith(".html")]
        for html_file in sorted(htmls):
            rel = os.path.join("projects", proj_id, html_file).replace("\\", "/")
            try:
                with io.open(os.path.join(pdir, html_file), "r", encoding="utf-8", errors="ignore") as fh:
                    txt = fh.read()
            except Exception:
                txt = ""
            meta = extract_meta(txt)
            items.append({
                "id": proj_id,
                "code": code,
                "name": name,
                "title": "Проект {} {}".format(code, name),
                "file": rel,
                "meta": {
                    "report_title": meta.get("title") or html_file,
                    "report_ts": meta.get("ts", "")
                }
            })
    write_json_utf8(items, OUT)
    print("Wrote {} item(s) to {}".format(len(items), OUT))

if __name__ == "__main__":
    main()
