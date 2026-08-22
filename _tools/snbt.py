# -*- coding: utf-8 -*-
"""Minimal SNBT / item-component-block parser + serializer.

Value model
-----------
Str(q, val)      quoted string, `q` is the original quote char
Word(text)       bare token: numbers (1b, 0.5f), booleans, unquoted ids, ~0.5 ...
Comp(items)      compound; items is a list of (key, value) where key is Str|Word
Lst(prefix,items) list / typed array; prefix is '', 'I;', 'L;' or 'B;'
Comps(entries)   item component block `id[a=b,!c,d]`; entries = [(name, value|None, negated)]
"""


class Node:
    pass


class Str(Node):
    __slots__ = ("q", "val")

    def __init__(self, q, val):
        self.q = q
        self.val = val

    def dump(self):
        q = self.q
        out = [q]
        for ch in self.val:
            if ch == q or ch == "\\":
                out.append("\\" + ch)
            else:
                out.append(ch)
        out.append(q)
        return "".join(out)


class Word(Node):
    __slots__ = ("text",)

    def __init__(self, text):
        self.text = text

    def dump(self):
        return self.text


class Comp(Node):
    __slots__ = ("items",)

    def __init__(self, items=None):
        self.items = items if items is not None else []

    # --- dict-ish helpers, matching on the *decoded* key text -------------
    def keytext(self, k):
        return k.val if isinstance(k, Str) else k.text

    def find(self, name):
        for i, (k, v) in enumerate(self.items):
            if self.keytext(k) == name:
                return i
        return -1

    def get(self, name, default=None):
        i = self.find(name)
        return self.items[i][1] if i >= 0 else default

    def pop(self, name, default=None):
        i = self.find(name)
        if i < 0:
            return default
        return self.items.pop(i)[1]

    def set(self, name, value):
        i = self.find(name)
        if i >= 0:
            self.items[i] = (self.items[i][0], value)
        else:
            self.items.append((Word(name), value))

    def has(self, name):
        return self.find(name) >= 0

    def dump(self):
        return "{" + ",".join(k.dump() + ":" + v.dump() for k, v in self.items) + "}"


class Lst(Node):
    __slots__ = ("prefix", "items")

    def __init__(self, prefix="", items=None):
        self.prefix = prefix
        self.items = items if items is not None else []

    def dump(self):
        return "[" + self.prefix + ",".join(v.dump() for v in self.items) + "]"


class Comps(Node):
    """`id[key=value,key~value,!key,key]` -- item components, item predicates
    and block states all share this bracket syntax.  `~` marks an item
    sub-predicate (partial match) rather than an exact component value."""

    __slots__ = ("entries",)

    def __init__(self, entries=None):
        # entries: [(name, value|None, negated, separator)]
        self.entries = entries if entries is not None else []

    def find(self, name):
        for i, e in enumerate(self.entries):
            if e[0] == name:
                return i
        return -1

    def dump(self):
        parts = []
        for name, value, neg, sep in self.entries:
            s = ("!" if neg else "") + name
            if value is not None:
                s += sep + value.dump()
            parts.append(s)
        return "[" + ",".join(parts) + "]"


class ParseError(Exception):
    pass


WS = " \t\r\n"
# characters that may appear in a bare SNBT token
WORD_CHARS = set("0123456789abcdefghijklmnopqrstuvwxyz"
                 "ABCDEFGHIJKLMNOPQRSTUVWXYZ_-.+#:/~^*")
# compound keys stop at ':' -- namespaced keys must be quoted (as vanilla writes them)
KEY_CHARS = WORD_CHARS - set(":")
# component / block-state / item-predicate names stop at the '=' or '~' separator
NAME_CHARS = WORD_CHARS - set("~*")


class Parser:
    def __init__(self, s, i=0):
        self.s = s
        self.i = i

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in WS:
            self.i += 1

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ""

    def expect(self, ch):
        if self.peek() != ch:
            raise ParseError("expected %r at %d in %r" % (ch, self.i, self.s[self.i:self.i + 40]))
        self.i += 1

    # ------------------------------------------------------------------
    def string(self):
        q = self.s[self.i]
        self.i += 1
        out = []
        while True:
            if self.i >= len(self.s):
                raise ParseError("unterminated string")
            ch = self.s[self.i]
            if ch == "\\":
                nxt = self.s[self.i + 1] if self.i + 1 < len(self.s) else ""
                if nxt in ('"', "'", "\\"):
                    out.append(nxt)
                    self.i += 2
                    continue
                # keep unknown escapes verbatim (\n, \uXXXX, ...)
                out.append(ch)
                out.append(nxt)
                self.i += 2
                continue
            if ch == q:
                self.i += 1
                return Str(q, "".join(out))
            out.append(ch)
            self.i += 1

    def word(self):
        start = self.i
        while self.i < len(self.s) and self.s[self.i] in WORD_CHARS:
            self.i += 1
        if self.i == start:
            raise ParseError("empty token at %d in %r" % (self.i, self.s[self.i:self.i + 40]))
        return Word(self.s[start:self.i])

    def value(self):
        self.ws()
        ch = self.peek()
        if ch == "{":
            return self.compound()
        if ch == "[":
            return self.list()
        if ch in ('"', "'"):
            return self.string()
        return self.word()

    def key(self):
        self.ws()
        if self.peek() in ('"', "'"):
            return self.string()
        start = self.i
        while self.i < len(self.s) and self.s[self.i] in KEY_CHARS:
            self.i += 1
        if self.i == start:
            raise ParseError("empty key at %d in %r" % (self.i, self.s[self.i:self.i + 40]))
        return Word(self.s[start:self.i])

    def compound(self):
        self.expect("{")
        items = []
        self.ws()
        if self.peek() == "}":
            self.i += 1
            return Comp(items)
        while True:
            k = self.key()
            self.ws()
            self.expect(":")
            v = self.value()
            items.append((k, v))
            self.ws()
            if self.peek() == ",":
                self.i += 1
                self.ws()
                if self.peek() == "}":     # tolerate trailing comma
                    self.i += 1
                    return Comp(items)
                continue
            self.expect("}")
            return Comp(items)

    def list(self):
        self.expect("[")
        prefix = ""
        # typed array prefix: [I; ...]
        if self.i + 1 < len(self.s) and self.s[self.i] in "ILB" and self.s[self.i + 1] == ";":
            prefix = self.s[self.i:self.i + 2]
            self.i += 2
        items = []
        self.ws()
        if self.peek() == "]":
            self.i += 1
            return Lst(prefix, items)
        while True:
            items.append(self.value())
            self.ws()
            if self.peek() == ",":
                self.i += 1
                self.ws()
                if self.peek() == "]":
                    self.i += 1
                    return Lst(prefix, items)
                continue
            self.expect("]")
            return Lst(prefix, items)

    # ------------------------------------------------------------------
    def component_block(self):
        """Parse `[a=b,!c,d]` starting at '['."""
        self.expect("[")
        entries = []
        self.ws()
        if self.peek() == "]":
            self.i += 1
            return Comps(entries)
        while True:
            self.ws()
            neg = False
            if self.peek() == "!":
                neg = True
                self.i += 1
                self.ws()
            start = self.i
            while self.i < len(self.s) and self.s[self.i] in NAME_CHARS:
                self.i += 1
            name = self.s[start:self.i]
            if not name:
                raise ParseError("empty component name at %d" % self.i)
            self.ws()
            value = None
            sep = "="
            if self.peek() in ("=", "~"):
                sep = self.peek()
                self.i += 1
                value = self.value()
            entries.append((name, value, neg, sep))
            self.ws()
            if self.peek() == ",":
                self.i += 1
                continue
            self.expect("]")
            return Comps(entries)


def parse_value(s, i=0):
    p = Parser(s, i)
    v = p.value()
    return v, p.i


def parse_component_block(s, i=0):
    p = Parser(s, i)
    v = p.component_block()
    return v, p.i
