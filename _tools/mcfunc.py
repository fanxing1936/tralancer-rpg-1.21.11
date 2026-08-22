# -*- coding: utf-8 -*-
"""Scan an .mcfunction line, find every NBT / component region, transform it."""

import re

from snbt import Parser, ParseError, Comp, Lst
import transform as T

SKIPPED = []          # regions the scanner could not parse (must stay empty)

SELECTOR_RE = re.compile(r"@[aeprsn]$")
WORDCH = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.-/:*#")

ATTR_CMD_RE = re.compile(r"\b(minecraft:)?(generic|player|horse|zombie)\.([a-z_]+)\b")


def skip_string(s, i):
    q = s[i]
    i += 1
    while i < len(s):
        if s[i] == "\\":
            i += 2
            continue
        if s[i] == q:
            return i + 1
        i += 1
    return i


def match_bracket(s, i):
    """i points at '[' or '{'; return index just past the matching close."""
    open_ch = s[i]
    close_ch = "]" if open_ch == "[" else "}"
    depth = 0
    while i < len(s):
        c = s[i]
        if c in ('"', "'"):
            i = skip_string(s, i)
            continue
        if c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return i


def selector_region(s, i):
    """Transform `nbt=` values inside a selector `[...]` that starts at i."""
    end = match_bracket(s, i)
    inner = s[i + 1:end - 1]
    out = []
    j = 0
    while j < len(inner):
        c = inner[j]
        if c in ('"', "'"):
            k = skip_string(inner, j)
            out.append(inner[j:k])
            j = k
            continue
        if inner.startswith("nbt=", j) and (j == 0 or inner[j - 1] in ", "):
            out.append("nbt=")
            j += 4
            if j < len(inner) and inner[j] == "!":
                out.append("!")
                j += 1
            try:
                p = Parser(inner, j)
                node = p.value()
                T.transform_nbt(node)
                out.append(node.dump())
                j = p.i
            except ParseError as exc:
                SKIPPED.append(("selector-nbt", str(exc)))
                out.append(inner[j])
                j += 1
            continue
        out.append(c)
        j += 1
    return "[" + "".join(out) + "]", end


def process(s):
    """Transform one command line (or any command-ish text)."""
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in ('"', "'"):
            k = skip_string(s, i)
            out.append(s[i:k])
            i = k
            continue
        if c == "{":
            try:
                p = Parser(s, i)
                node = p.compound()
                T.transform_nbt(node)
                out.append(node.dump())
                i = p.i
                continue
            except ParseError as exc:
                SKIPPED.append(("compound", str(exc)))
                out.append(c)
                i += 1
                continue
        if c == "[":
            prev2 = s[max(0, i - 2):i]
            if SELECTOR_RE.search(prev2):
                text, i = selector_region(s, i)
                out.append(text)
                continue
            prev = s[i - 1] if i else ""
            if prev in WORDCH:
                # item component block / block state
                try:
                    p = Parser(s, i)
                    block = p.component_block()
                    block = T.transform_component_block(block)
                    out.append(block.dump())
                    i = p.i
                    continue
                except ParseError as exc:
                    SKIPPED.append(("components", str(exc)))
                    out.append(c)
                    i += 1
                    continue
            else:
                # bare NBT list (tellraw / title component, typed array, ...)
                try:
                    p = Parser(s, i)
                    node = p.list()
                    T.transform_nbt(node)
                    out.append(node.dump())
                    i = p.i
                    continue
                except ParseError as exc:
                    SKIPPED.append(("list", str(exc)))
                    out.append(c)
                    i += 1
                    continue
        out.append(c)
        i += 1
    return "".join(out)


def attr_cmd_fix(line):
    """`attribute @s minecraft:generic.armor get` -> `minecraft:armor`."""
    def repl(m):
        ns = m.group(1) or ""
        T.bump("attribute id renamed")
        return ns + m.group(3)

    if line.lstrip().startswith("attribute ") or " run attribute " in line:
        return ATTR_CMD_RE.sub(repl, line)
    return line


def process_line(line):
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return line
    line = attr_cmd_fix(line)
    return process(line)
