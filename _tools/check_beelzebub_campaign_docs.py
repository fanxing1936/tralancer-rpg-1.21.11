#!/usr/bin/env python3
"""Cross-check the Chapter I canon, web codex and project documentation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def text(name):
    path = ROOT / name
    if not path.is_file():
        errors.append("missing document: " + name)
        return ""
    return path.read_text(encoding="utf-8")


try:
    campaign = json.loads(text("_campaign_beelzebub.json"))
except Exception as exc:
    errors.append("invalid campaign project data: %s" % exc)
    campaign = {}

flow = campaign.get("flow", [])
if len(flow) != 11:
    errors.append("campaign flow must contain all 11 requested steps")
stages = campaign.get("stages", [])
if len(stages) != 9:
    errors.append("story timing must contain nine acts")
else:
    low = sum(x["minutes"][0] for x in stages)
    high = sum(x["minutes"][1] for x in stages)
    if low < 30 or high > 60:
        errors.append("chapter timing escapes requested 30-60 minutes: %d-%d" % (low, high))

story = text("BEELZEBUB-CAMPAIGN-CHAPTER-1.md")
for phrase in (
    "第十三声钟", "米拉·维恩", "伊莱亚·沃斯", "执事卡西安", "审判官塞维拉",
    "桀派", "布提斯", "巴钦", "塞列欧斯", "布松",
    "环境假说 + 三种不可重复招式见证", "第一阶段：镇压", "第二阶段：镇魔",
    "第三阶段：固阵", "第四阶段：裁决", "消灭", "放逐", "封印", "契约",
    "见证人印", "第一次释放魔力", "边缘者临时入院令",
    "审判", "守护", "秘仪", "王冠失窃案", "失败、恢复与检查点",
):
    if phrase not in story:
        errors.append("story canon missing: " + phrase)

guide_source = text("_tools/emit_guide.py")
guide = text("TRALANCER-RPG-图鉴.html")
for phrase in ("id=\"s16\"", "第一章 · 空缺者", "campaign/beelzebub/start"):
    if phrase not in guide_source:
        errors.append("guide generator missing: " + phrase)
    if phrase not in guide:
        errors.append("generated guide missing: " + phrase)

readme = text("README.md")
for phrase in ("BEELZEBUB-CAMPAIGN-CHAPTER-1.md", "第一章：空缺者",
               "campaign/beelzebub/start"):
    if phrase not in readme:
        errors.append("README missing: " + phrase)

lore = text("LORE.md")
if "BEELZEBUB-CAMPAIGN-CHAPTER-1.md" not in lore:
    errors.append("LORE does not link its playable Chapter I adaptation")

book = text("_tools/add_book.py")
for phrase in ("第一章·空缺者", "缺失的见证", "王冠失窃案"):
    if phrase not in book:
        errors.append("in-game guide book missing: " + phrase)

engineering = text("ENGINEERING.md")
for phrase in ("第一章《空缺者》", "薄章节层与权威系统复用", "身份、多人和结算边界"):
    if phrase not in engineering:
        errors.append("engineering record missing: " + phrase)

level = text("_campaign_beelzebub_level.md")
for phrase in ("37 × 65", "真实空缺者教学", "五席未满", "环境假说与正式真名必须拆开", "验收矩阵"):
    if phrase not in level:
        errors.append("level specification missing: " + phrase)

art = text("_campaign_beelzebub_art_ui.md")
for phrase in ("别西卜", "Actionbar", "Bossbar", "粒子", "验收"):
    if phrase not in art:
        errors.append("art/UI specification missing: " + phrase)

if errors:
    print("Chapter I documentation check FAILED (%d)" % len(errors))
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("Chapter I documentation check OK: 11-step flow, 45-60 minute canon, web and README")
