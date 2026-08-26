# -*- coding: utf-8 -*-
"""Write the standalone debug-command handbook from the shared catalogue."""
from pathlib import Path
from debug_commands import render_markdown

ROOT = Path(__file__).resolve().parent.parent
(ROOT / "DEBUG-COMMANDS.md").write_text(render_markdown(), encoding="utf-8")
print("wrote ../DEBUG-COMMANDS.md")
