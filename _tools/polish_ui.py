# -*- coding: utf-8 -*-
"""全包文本的最终规范化：物品名、Lore 与七柱姓名色（ART-STYLE.md §1–§2）。

这个脚本必须放在所有内容生成器和 ``make_boxes.py`` 之后：领取箱会把完整
物品组件嵌进 ``container``，最后处理才能保证散装 give 与箱内副本完全一致。
作者 ``_orig`` 里的旧物品名不手改，也由这里统一。

规则全部来自 ``rpg_ui_style``：

* 物品名：方括号前缀换成规范标签（``[legend]`` → ``[传说]`` 等），加粗，
  取档次色；``[恶魔]``／``[契约]``／``[已立约]`` 取所属领主的亮色；
  本名一律白色、不加粗；所有片段显式 ``italic:false``——没写颜色的本名
  会被原版染成稀有度色（附魔过的普通物品是青色）。
* 七柱：任何文本组件里出现的七柱旧色（深色或旧亮色）统一换成该柱亮色；
  短标签式领主名也染成亮色。深色只作身份色，不写字。
* 物品名与 Lore 里其余达不到 4.5:1 的强调色按原色相提亮。
* 不改文字内容、技能名、数值或玩法；运行时没有任何逻辑按物品名匹配。
"""

import io
import json
import os
import re
import sys

import rpg_ui_style as ui


DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

# 七柱亮色：短标签式领主名染这个色。
DEMON_COLOURS = dict((p["who"], p["lit"]) for p in ui.PILLARS)

# 七柱的任何旧色（深色、旧亮色）出现在文本里 -> 该柱亮色。
LEGACY_TO_LIT = {}
for _p in ui.PILLARS:
    for _h in ui.PILLAR_LEGACY[_p["slug"]]:
        LEGACY_TO_LIT[_h.upper()] = _p["lit"]

# 同一个意思的近似色，合并到色板值。
NEAR_DUPLICATES = {
    "#FF7A70": ui.WARN, "#FF806B": ui.WARN, "#FF665E": ui.WARN,
    "#E8F8FF": ui.CYAN_LIGHT, "#F2FDFF": ui.CYAN_LIGHT, "#F3FDFF": ui.CYAN_LIGHT,
}

def _triplet(text):
    """'0.30, 0.0,0.6f' -> (0.3, 0.0, 0.6) so spellings compare equal."""
    return tuple(round(float(v.strip().rstrip("fF")), 2) for v in text.split(","))


DUST_LEGACY = {}
for _p in ui.PILLARS:
    for _role in ("lit", "deep"):
        for _f in ui.PILLAR_DUST_LEGACY[_p["slug"]][_role]:
            DUST_LEGACY[_triplet(_f)] = (_p, _role)
BLACK = (0.0, 0.0, 0.0)
DUST = re.compile(r'dust\{color:\[([^\]]+)\]')
DUST_TRANSITION = re.compile(r'dust_color_transition\{from_color:\[([^\]]+)\],to_color:\[([^\]]+)\]')

CUSTOM_NAME = re.compile(r'(?:(?:"minecraft:custom_name")|(?:\bcustom_name))\s*[:=]\s*')
LORE = re.compile(r'(?:(?:"minecraft:lore")|(?:\blore))\s*[:=]\s*')
SNBT_TEXT = re.compile(r'(?<!["\w])text\s*:\s*("(?:\\.|[^"\\])*")')
SNBT_COLOR = re.compile(r'(?<!["\w])color\s*:\s*("(?:\\.|[^"\\])*")')
SNBT_BOLD = re.compile(r'(?<!["\w])bold\s*:\s*(true|false)')
COLOUR_KEY = re.compile(r'((?:"color"|(?<![\w"])color)\s*:\s*")(#[0-9A-Fa-f]{6})"')
SENTENCE_MARKS = "，。；！？：\n"
PREFIX = re.compile(r"^\[[^\]\r\n]{1,20}\]$")


def is_name_label(value, who):
    """只把姓名标签上色，不把一整句正文染成别的颜色。"""
    value = value.strip()
    return (who in value and len(value) <= 20
            and not any(mark in value for mark in SENTENCE_MARKS))


def is_prefix(value):
    return bool(PREFIX.match(value.strip()))


def norm_colour(colour):
    if not isinstance(colour, str):
        return colour
    if colour.startswith("#"):
        colour = colour.upper()
        colour = LEGACY_TO_LIT.get(colour, colour)
        colour = NEAR_DUPLICATES.get(colour, colour)
    return colour


# ---------------------------------------------------------------------------
# 通用文本组件：七柱色与姓名标签
# ---------------------------------------------------------------------------
def polish_component(node, stats):
    if isinstance(node, list):
        for child in node:
            polish_component(child, stats)
        return
    if not isinstance(node, dict):
        return
    colour = node.get("color")
    if isinstance(colour, str):
        cooked = norm_colour(colour)
        if cooked != colour:
            node["color"] = cooked
            stats["colour_folded"] += 1
    value = node.get("text")
    if isinstance(value, str):
        for who, lit in DEMON_COLOURS.items():
            if is_name_label(value, who):
                if node.get("color") != lit:
                    node["color"] = lit
                    stats["demon_colour"] += 1
                # 文本样式会继承前一个/根组件：显式取消粗体，免得
                # 加粗的方括号前缀把领主本名也带成粗体。
                if not is_prefix(value) and node.get("bold") is not False:
                    node["bold"] = False
                stats["seen"][who] += 1
                break
    for key, child in list(node.items()):
        if key not in ("text", "color", "bold"):
            polish_component(child, stats)


def text_nodes(node):
    if isinstance(node, list):
        for child in node:
            for found in text_nodes(child):
                yield found
    elif isinstance(node, dict):
        if isinstance(node.get("text"), str):
            yield node
        for key, child in node.items():
            if key != "text":
                for found in text_nodes(child):
                    yield found


# ---------------------------------------------------------------------------
# 物品名
# ---------------------------------------------------------------------------
def prefix_style(tag, colour, name):
    """(规范标签, 颜色) for one bracket prefix of an item name."""
    key = ui.TAG_ALIASES.get(tag)
    if key == "devil":
        p = ui.pillar_in(name)
        return ui.tier_tag("devil"), p["lit"] if p else ui.readable(colour or "gray")
    if key:
        return ui.TIERS[key]
    tag = ui.MATERIAL_TAGS.get(tag, tag)
    if tag in ui.SYSTEM_TAGS:
        return tag, ui.SYSTEM_TAGS[tag]
    if tag in ("[契约]", "[已立约]"):
        p = ui.pillar_in(name)
        if p:
            return tag, p["lit"]
    return tag, ui.readable(norm_colour(colour) or "white")


def polish_item_name(component, stats):
    # 名字里的领主名只记数，不染色：本名一律白色。
    for node in text_nodes(component):
        for who in DEMON_COLOURS:
            if is_name_label(node.get("text", ""), who):
                stats["seen"][who] += 1
                break
    nodes = [n for n in text_nodes(component) if n.get("text", "").strip()]
    if not nodes:
        return
    head = nodes[0]
    rest = nodes[1:]
    name = "".join(n["text"] for n in rest)
    if is_prefix(head["text"]):
        tag, colour = prefix_style(head["text"].strip(), head.get("color"), name)
        if tag != head["text"]:
            stats["tag_renamed"] += 1
        head.update(text=tag, color=colour, bold=True, italic=False)
    else:
        rest = nodes
    for node in rest:
        if node.get("color") != ui.WHITE or node.get("bold") is not False:
            stats["name_white"] += 1
        node.update(color=ui.WHITE, bold=False, italic=False)


def polish_lore(lines, stats):
    for line in lines if isinstance(lines, list) else []:
        for node in text_nodes(line):
            colour = node.get("color")
            if isinstance(colour, str):
                lifted = ui.readable(norm_colour(colour))
                if lifted != ui.hex_of(colour) and lifted != colour:
                    node["color"] = lifted
                    stats["lore_lifted"] += 1
            if "italic" not in node:
                node["italic"] = False


# ---------------------------------------------------------------------------
# mcfunction 扫描
# ---------------------------------------------------------------------------
def matching_bracket(text, start):
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        ch = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return pos
    return -1


def regions(pattern, text):
    for match in pattern.finditer(text):
        start = match.end()
        while start < len(text) and text[start].isspace():
            start += 1
        if start >= len(text) or text[start] != "[":
            continue
        end = matching_bracket(text, start)
        if end < 0:
            continue
        yield start, end + 1, text[start:end + 1]


def custom_name_regions(text):
    return regions(CUSTOM_NAME, text)


BOOK = re.compile(r'(?:minecraft:)?(?:written|writable)_book_content\s*[:=]\s*\{')


def book_spans(text):
    """书页是浅色纸面，深色墨水才读得出 —— 七柱深色在这里是对的，不折叠。"""
    spans = []
    for match in BOOK.finditer(text):
        depth, quoted, escaped = 0, False, False
        for pos in range(match.end() - 1, len(text)):
            ch = text[pos]
            if quoted:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quoted = False
                continue
            if ch == '"':
                quoted = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    spans.append((match.start(), pos + 1))
                    break
    return spans


def leaf_objects(text):
    """线性找出不含子对象的 ``{...}``，避免超长领取箱上的正则回溯。"""
    stack = []
    quoted = False
    escaped = False
    for pos, ch in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "{":
            if stack:
                stack[-1][1] = True
            stack.append([pos, False])
        elif ch == "}" and stack:
            start, has_child = stack.pop()
            if not has_child:
                yield start, pos + 1, text[start:pos + 1]


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def polish_regions(text, pattern, handler, stats):
    edits = []
    for start, end, raw in regions(pattern, text):
        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            stats["unparsed"].append(raw[:80])
            continue
        polish_component(value, stats)
        handler(value, stats)
        cooked = dump(value)
        if cooked != raw:
            edits.append((start, end, cooked))
    for start, end, cooked in reversed(edits):
        text = text[:start] + cooked + text[end:]
    return text, [(s, e) for s, e, _ in edits]


def polish_leaf(raw, stats):
    if '"text"' not in raw:
        # 旧书页仍可能使用合法 SNBT 的未加引号键：{text:"玛门",color:"aqua"}
        field = SNBT_TEXT.search(raw)
        if not field:
            return raw
        try:
            value = json.loads(field.group(1))
        except (TypeError, ValueError):
            return raw
        colour_field = SNBT_COLOR.search(raw)
        current = json.loads(colour_field.group(1)) if colour_field else None
        wanted = norm_colour(current)
        for who, lit in DEMON_COLOURS.items():
            if is_name_label(value, who):
                stats["seen"][who] += 1
                wanted = lit
                break
        if wanted == current or wanted is None:
            return raw
        stats["colour_folded"] += 1
        if colour_field:
            return (raw[:colour_field.start(1)] + json.dumps(wanted)
                    + raw[colour_field.end(1):])
        return raw[:-1] + ",color:" + json.dumps(wanted) + "}"
    try:
        component = json.loads(raw)
    except (TypeError, ValueError):
        return raw
    before = dump(component)
    polish_component(component, stats)
    after = dump(component)
    return raw if before == after else after


def process_mcfunction(path, stats):
    with io.open(path, encoding="utf-8") as handle:
        source = handle.read()
    # 先处理散落的文本组件（跳过物品名：本名必须保持白色，不能被
    # 当成领主姓名标签染色），再让物品名与 Lore 规则最后落定。
    names = [(s, e) for s, e, _ in custom_name_regions(source)]
    books = book_spans(source)
    edits = []
    for start, end, raw in leaf_objects(source):
        if any(lo <= start < hi for lo, hi in names + books):
            continue
        cooked = polish_leaf(raw, stats)
        if cooked != raw:
            edits.append((start, end, cooked))
    text = source
    for start, end, cooked in reversed(edits):
        text = text[:start] + cooked + text[end:]
    # 带点击事件等子对象的组件不是叶子；颜色键只会是文本色（粒子色是
    # 数组），所以剩下的旧色直接按键值折叠。
    def fold(match):
        cooked = norm_colour(match.group(2))
        if cooked != match.group(2).upper():
            stats["colour_folded"] += 1
            return match.group(1) + cooked + '"'
        return match.group(0)
    books = book_spans(text)
    text = COLOUR_KEY.sub(
        lambda m: m.group(0) if any(lo <= m.start() < hi for lo, hi in books) else fold(m),
        text)
    text = polish_dust(text, stats)
    text, _ = polish_regions(text, CUSTOM_NAME, polish_item_name, stats)
    text, _ = polish_regions(text, LORE, polish_lore, stats)
    if text != source:
        with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        stats["files"] += 1


# ---------------------------------------------------------------------------
# 粒子：七柱旧色 -> 色板（ART-STYLE.md §6）
# ---------------------------------------------------------------------------
def polish_dust(text, stats):
    """作者原件与模板里的七柱粒子色统一到色板：单色用亮色，渐变取
    「亮 -> 深」；跟在七柱色后面的纯黑暗端也换成该柱深色。与七柱无关的
    武器粒子（夜、樱、星……）是作者的设计，不动。"""
    def single(match):
        hit = DUST_LEGACY.get(_triplet(match.group(1)))
        if not hit:
            return match.group(0)
        stats["dust_folded"] += 1
        return "dust{color:[%s]" % ui.floats(hit[0]["lit"])

    def pair(match):
        a, b = _triplet(match.group(1)), _triplet(match.group(2))
        hit = DUST_LEGACY.get(a) or DUST_LEGACY.get(b)
        if not hit:
            return match.group(0)
        p = hit[0]
        if b not in DUST_LEGACY and b != BLACK:
            # 起点是七柱色、终点是别的设计色：只换起点。
            start, end = ui.floats(p["lit"]), match.group(2)
        else:
            start, end = ui.floats(p["lit"]), ui.floats(p["deep"])
        stats["dust_folded"] += 1
        return "dust_color_transition{from_color:[%s],to_color:[%s]" % (start, end)

    text = DUST.sub(single, text)
    return DUST_TRANSITION.sub(pair, text)


# ---------------------------------------------------------------------------
# JSON（战利品表、物品修饰器、进度）
# ---------------------------------------------------------------------------
def walk_json(node, stats):
    if isinstance(node, list):
        for child in node:
            walk_json(child, stats)
        return
    if not isinstance(node, dict):
        return
    for key, child in node.items():
        if key == "minecraft:custom_name" or (key == "name" and
                                              node.get("function") == "minecraft:set_name"):
            polish_item_name(child, stats)
        elif key == "minecraft:lore" or (key == "lore" and
                                         node.get("function") == "minecraft:set_lore"):
            polish_lore(child, stats)
        else:
            walk_json(child, stats)


def process_json(path, stats):
    with io.open(path, encoding="utf-8") as handle:
        doc = json.load(handle)
    before = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    polish_component(doc, stats)
    walk_json(doc, stats)
    after = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    if before != after:
        with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(doc, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        stats["files"] += 1


# ---------------------------------------------------------------------------
# 末端断言
# ---------------------------------------------------------------------------
OLD_TAGS = set(ui.MATERIAL_TAGS) | set(
    tag for tag, key in ui.TAG_ALIASES.items() if tag != ui.TIERS[key][0])


def validate(stats):
    missing = [who for who, count in stats["seen"].items() if count == 0]
    if missing:
        raise SystemExit("未发现恶魔姓名组件：" + "、".join(missing))
    problems = []
    legacy = set(LEGACY_TO_LIT) | set(NEAR_DUPLICATES)
    colour_field = re.compile(r'"color"\s*:\s*"(#[0-9A-Fa-f]{6})"')
    for root, _, files in os.walk(DP):
        for name in files:
            if not name.endswith(".mcfunction"):
                continue
            path = os.path.join(root, name)
            data = io.open(path, encoding="utf-8").read()
            for lo, hi in reversed(book_spans(data)):
                data = data[:lo] + data[hi:]
            for found in colour_field.findall(data):
                if found.upper() in legacy:
                    problems.append("%s: 旧色 %s 仍在写字" % (path, found))
            for _, _, raw in custom_name_regions(data):
                try:
                    value = json.loads(raw)
                except (TypeError, ValueError):
                    continue
                nodes = [n for n in text_nodes(value) if n.get("text", "").strip()]
                for i, node in enumerate(nodes):
                    text = node["text"].strip()
                    if i == 0 and is_prefix(text):
                        if text in OLD_TAGS:
                            problems.append("%s: 旧标签 %s" % (path, text))
                        if ui.contrast(node.get("color", "white")) < 4.5:
                            problems.append("%s: 前缀 %s 对比度不足" % (path, text))
                        continue
                    if node.get("color") != ui.WHITE or node.get("bold") is not False:
                        problems.append("%s: 本名 %s 不是白色或仍加粗" % (path, text))
    if problems:
        raise SystemExit("文本规范仍有残留：\n" + "\n".join(problems[:30]))


def main():
    stats = {
        "files": 0, "tag_renamed": 0, "name_white": 0, "lore_lifted": 0,
        "colour_folded": 0, "demon_colour": 0, "dust_folded": 0, "unparsed": [],
        "seen": dict((who, 0) for who in DEMON_COLOURS),
    }
    for root, dirs, files in os.walk(DP):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(root, name)
            if name.endswith(".mcfunction"):
                process_mcfunction(path, stats)
            elif name.endswith(".json"):
                process_json(path, stats)
    validate(stats)
    print("物品名：%d 个前缀换成规范标签，%d 个本名改为白色" % (
        stats["tag_renamed"], stats["name_white"]))
    print("七柱色：%d 处旧色并入色板，%d 处领主名染亮色；命中 %s" % (
        stats["colour_folded"], stats["demon_colour"], ", ".join(
            "%s=%d" % pair for pair in stats["seen"].items())))
    print("粒子：%d 处七柱旧色并入色板" % stats["dust_folded"])
    print("Lore：%d 处强调色提亮到 4.5:1；共改 %d 文件" % (
        stats["lore_lifted"], stats["files"]))
    if stats["unparsed"]:
        print("跳过 %d 处非 JSON 文本（SNBT）：%s" % (
            len(stats["unparsed"]), stats["unparsed"][0]))


if __name__ == "__main__":
    main()
