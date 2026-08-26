# -*- coding: utf-8 -*-
"""Keep endless-mode documentation and the generated codex in sync."""
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
files = {
    "guide": ROOT / "ENDLESS-EXORCISM.md",
    "readme": ROOT / "README.md",
    "engineering": ROOT / "ENGINEERING.md",
    "html": ROOT / "TRALANCER-RPG-图鉴.html",
}
errors = []
texts = {}
for name, path in files.items():
    if not path.is_file():
        errors.append(f"missing {name}: {path.name}")
        texts[name] = ""
    else:
        texts[name] = path.read_text(encoding="utf-8")

contracts = {
    "guide": ("72 套", "37 位游离魔神", "每 5 层", "圣恩", "断罪", "遗珍", "第 100 层", "_endless_exorcism_config.json"),
    "readme": ("七柱回廊", "完整 72 柱", "rpg:endless/start", "ENDLESS-EXORCISM.md"),
    "engineering": ("有限内容的无尽组合", "rpg_end_id", "check_endless_exorcism.py"),
    "html": ('id="s17"', "无尽驱魔 · 七柱回廊", "rpg:endless/debug/menu", "领主层"),
}
for name, signatures in contracts.items():
    for signature in signatures:
        if signature not in texts[name]:
            errors.append(f"{name} missing: {signature}")

if errors:
    print(f"Endless documentation check FAILED ({len(errors)})")
    for error in errors:
        print("- " + error)
    raise SystemExit(1)
print("Endless documentation check OK: rules, config, README and web codex")
