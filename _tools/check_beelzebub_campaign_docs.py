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
    "第十三声钟", "调查叙事与解谜结构", "第一层误导", "第二层误导", "四次阶段复盘",
    "米拉·维恩", "伊莱亚·沃斯", "执事卡西安", "审判官塞维拉",
    "桀派", "布提斯", "巴钦", "塞列欧斯", "布松",
    "环境假说 + 三种不可重复招式见证", "第一阶段：镇压", "第二阶段：镇魔",
    "第三阶段：固阵", "第四阶段：裁决", "消灭", "放逐", "封印", "契约",
    "见证人印", "第一次释放魔力", "边缘者临时入院令",
    "审判", "守护", "秘仪", "王冠失窃案", "失败、恢复与检查点",
    "塞维拉下令删证，卡西安执行清洗，别西卜借空缺进食；三者同时成立",
):
    if phrase not in story:
        errors.append("story canon missing: " + phrase)

guide_source = text("_tools/emit_guide.py")
guide = text("TRALANCER-RPG-图鉴.html")
for phrase in ("id=\"s16\"", "第一章 · 空缺者", "campaign/beelzebub/start",
               "楔子 · 第十三声钟", "观察 → 竞争解释 → 交叉验证 → 复盘", "随时复盘"):
    if phrase not in guide_source:
        errors.append("guide generator missing: " + phrase)
    if phrase not in guide:
        errors.append("generated guide missing: " + phrase)

investigation = campaign.get("investigation", {})
if investigation.get("loop") != ["观察事实", "保留竞争解释", "交叉验证", "阶段复盘"]:
    errors.append("campaign investigation loop is incomplete")
if len(investigation.get("misdirections", [])) < 2:
    errors.append("campaign needs at least two deliberate misdirections")
if len(investigation.get("cross_validation", [])) < 3:
    errors.append("campaign cross-validation layers are incomplete")
if "三者同时成立" not in investigation.get("chapter_summary", ""):
    errors.append("campaign lacks a player-repeatable final summary")
runtime_config = campaign.get("runtime_config", {})
if runtime_config.get("source") != "_campaign_beelzebub_config.json" or runtime_config.get("debug_menu") != "rpg:campaign/beelzebub/debug/menu":
    errors.append("campaign project data does not link the runtime configuration")

readme = text("README.md")
for phrase in ("BEELZEBUB-CAMPAIGN-CHAPTER-1.md", "第一章：空缺者",
               "campaign/beelzebub/start", "_campaign_beelzebub_config.json",
               "campaign/beelzebub/debug/menu"):
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
for phrase in ("第一章《空缺者》", "薄章节层与权威系统复用", "身份、多人和结算边界",
               "叙事循环、统一配置与调试台", "data/rpg/chapter/beelzebub_config.json"):
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

config_doc = text("BEELZEBUB-CAMPAIGN-CONFIG.md")
for phrase in ("_campaign_beelzebub_config.json", "24 个相对位置", "debug/menu", "stage/<0..10>"):
    if phrase not in config_doc:
        errors.append("campaign config documentation missing: " + phrase)

for phrase in ("_campaign_beelzebub_config.json", "campaign/beelzebub/debug/menu", "统一配置"):
    if phrase not in guide_source:
        errors.append("guide generator missing config/debug note: " + phrase)

if errors:
    print("Chapter I documentation check FAILED (%d)" % len(errors))
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("Chapter I documentation check OK: 11-step flow, 45-60 minute canon, web and README")
