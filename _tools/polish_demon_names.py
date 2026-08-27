# -*- coding: utf-8 -*-
"""统一七罪姓名色，并清理物品名后缀的粗体。

这个脚本必须放在所有内容生成器和 ``make_boxes.py`` 之后：领取箱会把完整
物品组件嵌进 ``container``，最后处理才能保证散装 give 与箱内副本完全一致。

规则很窄：

* 短标签式恶魔姓名使用契约主色；罪器本名例外保留青色，契约柱名用白色；
* 方括号前缀可以继续加粗；恶魔本名与物品 ``custom_name`` 的其余后缀强制不加粗；
* 不改 lore 的强调，不改技能名、数值或玩法。
"""

import io
import json
import os
import re
import sys


DP = sys.argv[1] if len(sys.argv) > 1 else "../rpg"

# 契约与罪器共同使用的七罪身份色。全部规范为 #RRGGBB。
DEMON_COLOURS = {
    "路西法": "#00491C",
    "利维坦": "#1B4F72",
    "亚巴顿": "#6A6A70",
    "别西卜": "#5A6B1E",
    "萨麦尔": "#7B241C",
    "贝利尔": "#5B2C6F",
    "玛门": "#B7950B",
}

# 物品名是唯一的上下文例外：罪器保留经典青色本名，契约柱名保持白色；
# 方括号前缀继续使用各生成器给出的罪器色/契约色。
ITEM_SUFFIX_COLOURS = {
    "[DEVIL]": "#55FFFF",
    "[契约]": "#FFFFFF",
    "[已立约]": "#FFFFFF",
}

CUSTOM_NAME = re.compile(r'(?:(?:"minecraft:custom_name")|(?:\bcustom_name))\s*[:=]\s*')
SNBT_TEXT = re.compile(r'(?<!["\w])text\s*:\s*("(?:\\.|[^"\\])*")')
SNBT_COLOR = re.compile(r'(?<!["\w])color\s*:\s*("(?:\\.|[^"\\])*")')
SNBT_BOLD = re.compile(r'(?<!["\w])bold\s*:\s*(true|false)')
SENTENCE_MARKS = "，。；！？：\n"


def is_name_label(value, who):
    """只把姓名标签上色，不把一整句正文染成深色。"""
    value = value.strip()
    return (who in value and len(value) <= 20
            and not any(mark in value for mark in SENTENCE_MARKS))


def is_prefix(value):
    value = value.strip()
    return bool(re.match(r"^\[[^\]\r\n]{1,20}\]$", value))


def polish_component(node, *, item_name=False, colour_names=True, stats=None):
    if isinstance(node, list):
        for child in node:
            polish_component(child, item_name=item_name,
                             colour_names=colour_names, stats=stats)
        return
    if not isinstance(node, dict):
        return

    value = node.get("text")
    if isinstance(value, str) and colour_names:
        for who, colour in DEMON_COLOURS.items():
            if is_name_label(value, who):
                if node.get("color") != colour:
                    node["color"] = colour
                    stats["demon_colour"] += 1
                # Text-component styles inherit from the preceding/root
                # component.  Be explicit so a bold [DEVIL] prefix cannot
                # make the proper name bold as well.
                if not is_prefix(value) and node.get("bold") is not False:
                    node["bold"] = False
                    stats["demon_unbold"] += 1
                stats["seen"][who] += 1
                break

        # 方括号稀有度/阵营前缀保留强调；真正的物品名永不继承粗体。
    if isinstance(value, str):
        if item_name and not is_prefix(value) and node.get("bold") is not False:
            if node.get("bold") is True:
                stats["suffix_unbold"] += 1
            node["bold"] = False

    for key, child in list(node.items()):
        if key not in ("text", "color", "bold"):
            polish_component(child, item_name=item_name,
                             colour_names=colour_names, stats=stats)


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


def polish_named_item(component, stats):
    nodes = list(text_nodes(component))
    prefix = next((node.get("text", "").strip() for node in nodes
                   if node.get("text", "").strip() in ITEM_SUFFIX_COLOURS), None)
    if not prefix:
        return
    suffix_colour = ITEM_SUFFIX_COLOURS[prefix]
    for node in nodes:
        value = node.get("text", "").strip()
        if not value or value == prefix or is_prefix(value):
            continue
        if node.get("color") != suffix_colour:
            node["color"] = suffix_colour
            stats["item_suffix_colour"] += 1


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


def custom_name_regions(text):
    for match in CUSTOM_NAME.finditer(text):
        start = match.end()
        while start < len(text) and text[start].isspace():
            start += 1
        if start >= len(text) or text[start] != "[":
            continue
        end = matching_bracket(text, start)
        if end < 0:
            continue
        yield start, end + 1, text[start:end + 1]


def polish_snbt_item_name(raw, stats):
    edits = []
    for start, end, leaf in leaf_objects(raw):
        field = SNBT_TEXT.search(leaf)
        if not field:
            continue
        try:
            value = json.loads(field.group(1))
        except (TypeError, ValueError):
            continue
        if is_prefix(value):
            continue
        bold = SNBT_BOLD.search(leaf)
        if bold:
            if bold.group(1) == "true":
                stats["suffix_unbold"] += 1
            cooked = leaf[:bold.start(1)] + "false" + leaf[bold.end(1):]
        else:
            cooked = leaf[:-1] + ",bold:false}"
        if cooked != leaf:
            edits.append((start, end, cooked))
    for start, end, cooked in reversed(edits):
        raw = raw[:start] + cooked + raw[end:]
    return raw


def polish_custom_names(text, stats):
    edits = []
    for start, end, raw in custom_name_regions(text):
        try:
            component = json.loads(raw)
        except (TypeError, ValueError):
            cooked = polish_snbt_item_name(raw, stats)
        else:
            target = any(node.get("text", "").strip() in ITEM_SUFFIX_COLOURS
                         for node in text_nodes(component))
            polish_component(component, item_name=True,
                             colour_names=not target, stats=stats)
            polish_named_item(component, stats)
            cooked = json.dumps(component, ensure_ascii=False, separators=(",", ":"))
        if cooked != raw:
            edits.append((start, end, cooked))

    for start, end, cooked in reversed(edits):
        text = text[:start] + cooked + text[end:]
    stats["custom_names"] += len(edits)
    return text


def custom_name_arrays(text):
    """读出命令中可解析的物品 custom_name 数组，供末端断言复用。"""
    for _, _, raw in custom_name_regions(text):
        try:
            yield json.loads(raw)
        except (TypeError, ValueError):
            continue


def bold_suffixes(node, found):
    if isinstance(node, list):
        for child in node:
            bold_suffixes(child, found)
    elif isinstance(node, dict):
        value = node.get("text")
        if (isinstance(value, str) and not is_prefix(value)
                and node.get("bold") is True):
            found.append(value)
        for key, child in node.items():
            if key not in ("text", "bold"):
                bold_suffixes(child, found)


def polish_leaf(match, stats):
    raw = match
    if '"text"' not in raw:
        # 旧书页仍可能使用合法 SNBT 的未加引号键：
        # {text:"玛门的弓",color:"aqua"}。它不是 JSON，但也是文本组件。
        field = SNBT_TEXT.search(raw)
        if not field:
            return raw
        try:
            value = json.loads(field.group(1))
        except (TypeError, ValueError):
            return raw
        for who, colour in DEMON_COLOURS.items():
            if not is_name_label(value, who):
                continue
            stats["seen"][who] += 1
            colour_field = SNBT_COLOR.search(raw)
            replacement = json.dumps(colour)
            if colour_field:
                current = json.loads(colour_field.group(1))
                if current == colour:
                    return raw
                stats["demon_colour"] += 1
                return (raw[:colour_field.start(1)] + replacement
                        + raw[colour_field.end(1):])
            stats["demon_colour"] += 1
            return raw[:-1] + ",color:" + replacement + "}"
        return raw
    try:
        component = json.loads(raw)
    except (TypeError, ValueError):
        return raw
    before = json.dumps(component, ensure_ascii=False, sort_keys=True)
    polish_component(component, stats=stats)
    after = json.dumps(component, ensure_ascii=False, sort_keys=True)
    if before == after:
        return raw
    return json.dumps(component, ensure_ascii=False, separators=(",", ":"))


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


def polish_leaf_objects(text, stats, skip_spans=()):
    edits = []
    for start, end, raw in leaf_objects(text):
        if any(lo <= start < hi for lo, hi in skip_spans):
            continue
        cooked = polish_leaf(raw, stats)
        if cooked != raw:
            edits.append((start, end, cooked))
    for start, end, cooked in reversed(edits):
        text = text[:start] + cooked + text[end:]
    return text


def process_mcfunction(path, stats):
    # These components are exact historical matching keys, not displayed UI.
    if path.replace('\\', '/').endswith('/prayer/currency.mcfunction'):
        return
    with io.open(path, encoding="utf-8") as handle:
        source = handle.read()
    # 先统一普通姓名，再让物品上下文最后覆盖罪器青色/契约白色例外。
    item_spans = [(start, end) for start, end, _ in custom_name_regions(source)]
    result = polish_leaf_objects(source, stats, item_spans)
    result = polish_custom_names(result, stats)
    if result != source:
        with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(result)
        stats["files"] += 1


def process_json(path, stats):
    with io.open(path, encoding="utf-8") as handle:
        doc = json.load(handle)
    before = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    polish_component(doc, stats=stats)
    after = json.dumps(doc, ensure_ascii=False, sort_keys=True)
    if before != after:
        with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(doc, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        stats["files"] += 1


def validate(stats):
    missing = [who for who, count in stats["seen"].items() if count == 0]
    if missing:
        raise SystemExit("未发现恶魔姓名组件：" + "、".join(missing))

    # 二次扫描所有可解析的短姓名组件，保证不存在遗留的原版命名色或旧亮色。
    wrong = []
    bold = []
    for root, _, files in os.walk(DP):
        for name in files:
            if not name.endswith(".mcfunction"):
                continue
            path = os.path.join(root, name)
            if path.replace('\\', '/').endswith('/prayer/currency.mcfunction'):
                continue
            data = io.open(path, encoding="utf-8").read()
            regions = list(custom_name_regions(data))
            for _, _, raw_name in regions:
                try:
                    item_name = json.loads(raw_name)
                except (TypeError, ValueError):
                    continue
                names = []
                bold_suffixes(item_name, names)
                bold.extend("%s: %s" % (path, value) for value in names)
                nodes = list(text_nodes(item_name))
                prefix = next((node.get("text", "").strip() for node in nodes
                               if node.get("text", "").strip() in ITEM_SUFFIX_COLOURS), None)
                for node in nodes:
                    value = node.get("text")
                    if not isinstance(value, str):
                        continue
                    for who, colour in DEMON_COLOURS.items():
                        if not is_name_label(value, who):
                            continue
                        expected = (ITEM_SUFFIX_COLOURS[prefix]
                                    if prefix and value.strip() != prefix else colour)
                        if node.get("color") != expected:
                            wrong.append("%s: %s -> %r (应为 %s)" %
                                         (path, value, node.get("color"), expected))
                        break
            for _, _, item_name in regions:
                for _, _, leaf in leaf_objects(item_name):
                    field = SNBT_TEXT.search(leaf)
                    bold_field = SNBT_BOLD.search(leaf)
                    if not field or not bold_field or bold_field.group(1) != "true":
                        continue
                    try:
                        value = json.loads(field.group(1))
                    except (TypeError, ValueError):
                        continue
                    if not is_prefix(value):
                        bold.append("%s: %s" % (path, value))
            spans = [(start, end) for start, end, _ in regions]
            for start, _, raw in leaf_objects(data):
                if any(lo <= start < hi for lo, hi in spans):
                    continue
                try:
                    component = json.loads(raw)
                except (TypeError, ValueError):
                    field = SNBT_TEXT.search(raw)
                    if not field:
                        continue
                    try:
                        value = json.loads(field.group(1))
                    except (TypeError, ValueError):
                        continue
                    colour_field = SNBT_COLOR.search(raw)
                    current = (json.loads(colour_field.group(1))
                               if colour_field else None)
                    for who, colour in DEMON_COLOURS.items():
                        if is_name_label(value, who) and current != colour:
                            wrong.append("%s: %s -> %r" % (path, value, current))
                            break
                    continue
                value = component.get("text") if isinstance(component, dict) else None
                if not isinstance(value, str):
                    continue
                for who, colour in DEMON_COLOURS.items():
                    if is_name_label(value, who) and component.get("color") != colour:
                        wrong.append("%s: %s -> %r" % (path, value, component.get("color")))
                    if is_name_label(value, who) and not is_prefix(value) and component.get("bold") is not False:
                        bold.append("%s: %s" % (path, value))
                        break
    if wrong:
        raise SystemExit("恶魔姓名色仍有残留：\n" + "\n".join(wrong[:20]))
    if bold:
        raise SystemExit("物品名后缀仍有粗体：\n" + "\n".join(bold[:20]))


def main():
    stats = {
        "files": 0,
        "custom_names": 0,
        "suffix_unbold": 0,
        "item_suffix_colour": 0,
        "demon_colour": 0,
        "demon_unbold": 0,
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
    print("恶魔姓名色：%d 处更新；七罪命中 %s" % (
        stats["demon_colour"], ", ".join(
            "%s=%d" % pair for pair in stats["seen"].items())))
    print("恶魔本名字重：%d 处显式取消粗体继承" % stats["demon_unbold"])
    print("物品名：%d 个 custom_name 规范化，%d 个后缀取消粗体；共改 %d 文件" % (
        stats["custom_names"], stats["suffix_unbold"], stats["files"]))
    print("物品双色：%d 个罪器/契约本名更新（罪器 #55FFFF，契约 #FFFFFF）" %
          stats["item_suffix_colour"])


if __name__ == "__main__":
    main()
