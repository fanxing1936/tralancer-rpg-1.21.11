# -*- coding: utf-8 -*-
"""序章台词表：从 Claude Docs 的《破碎大陆》序章 · 脚本书导出 `_tools/prologue_ref/lines.json`。

    python prologue_lines.py <docs read 的结果文件>     # 结果是 {"data":{"xml":...}} 的 JSON

脚本书是唯一原稿（用户 2026-11-22）：改词只改文档，再重新导出；这里不手抄任何台词。
凡是首列表头为「编号」的表格都收：编号、说话人、中文、English、配音提示、时长/触发等列按表头取。
是否配音：对话类（D/M/E/X/L）全部配；旁白只配开场五句 N01～N05；界面文字（U/T/R）不配。
"""
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "prologue_ref", "lines.json")

SPEAKERS = {"旁白": "narrator", "路西法": "lucifer", "米迦勒": "michael", "别西卜": "beelzebub",
            "贝利尔": "belial", "玛门": "mammon", "敌基督": "antichrist", "—": None}
VOICED_NARRATION = {"N01", "N02", "N03", "N04", "N05"}


def text_of(el):
    return "".join(t.text or "" for t in el.iter("text")).strip()


def tables(xml):
    root = ET.fromstring(xml)
    for tb in root.iter("table"):
        rows = [[text_of(c) for c in r.findall("cell")] for r in tb.findall("row")]
        if rows and rows[0] and rows[0][0] == "编号":
            yield rows


def main(path):
    raw = io.open(path, encoding="utf-8").read()
    data = json.loads(raw.splitlines()[0])      # 读取结果后面还跟着一段说明文字
    xml = data["data"]["xml"] if "data" in data else data["xml"]
    lines, seen = [], set()
    for rows in tables(xml):
        head = rows[0]
        for r in rows[1:]:
            rec = dict(zip(head, r))
            lid = rec.get("编号", "").strip()
            if not re.fullmatch(r"[A-Z]\d\d", lid) or lid in seen:
                continue
            seen.add(lid)
            who = rec.get("说话人", "—" if lid[0] in "UTR" else "旁白").strip() or "—"
            kind = lid[0]
            voiced = (kind in "DMEXL") or (lid in VOICED_NARRATION)
            lines.append({
                "id": lid,
                "speaker": SPEAKERS.get(who, who),
                "speaker_zh": None if who == "—" else who,
                "zh": rec.get("中文", "").strip(),
                "en": rec.get("English", "").strip(),
                "direction": (rec.get("配音提示") or rec.get("配音提示（若配）") or "").strip().strip("—") or None,
                "when": (rec.get("何时出现") or rec.get("触发") or rec.get("用在") or "").strip() or None,
                "est": (rec.get("时长") or "").strip() or None,
                "voiced": voiced,
            })
    order = "UNTDMLEXR"
    lines.sort(key=lambda x: (order.index(x["id"][0]), x["id"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(
        {"source": "《破碎大陆》序章 · 脚本书 (Claude Docs 698022a6-36e3-432b-850d-6247c01c505b)",
         "lines": lines}, ensure_ascii=False, indent=1) + "\n")
    v = [x for x in lines if x["voiced"]]
    print("lines %d, voiced %d -> %s" % (len(lines), len(v), OUT))
    for x in lines:
        if not x["zh"] or not x["en"]:
            print("  missing text:", x["id"])


if __name__ == "__main__":
    main(sys.argv[1])
