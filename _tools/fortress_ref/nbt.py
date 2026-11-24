# -*- coding: utf-8 -*-
"""Pure-Python Minecraft NBT (gzip/raw) and Anvil (.mca) reader/writer.

Zero external dependencies; supports all 12 NBT tag types with explicit typed
wrappers so round-tripping preserves exact tag types (Byte/Short/Int/Long,
Float/Double, arrays, typed lists).
"""

import gzip
import io
import os
import struct
import zlib

TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12


class Tag:
    tag_id = -1

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.value)

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.tag_id == other.tag_id and self.value == other.value
        return self.value == other


class Byte(Tag):
    tag_id = TAG_BYTE


class Short(Tag):
    tag_id = TAG_SHORT


class Int(Tag):
    tag_id = TAG_INT


class Long(Tag):
    tag_id = TAG_LONG


class Float(Tag):
    tag_id = TAG_FLOAT


class Double(Tag):
    tag_id = TAG_DOUBLE


class ByteArray(Tag):
    tag_id = TAG_BYTE_ARRAY


class String(Tag):
    tag_id = TAG_STRING


class IntArray(Tag):
    tag_id = TAG_INT_ARRAY


class LongArray(Tag):
    tag_id = TAG_LONG_ARRAY


class List(Tag):
    tag_id = TAG_LIST

    def __init__(self, elem_type, items=None):
        self.elem_type = elem_type
        self.value = list(items) if items is not None else []

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, idx):
        return self.value[idx]

    def append(self, item):
        self.value.append(item)

    def __repr__(self):
        return "List(%d, %r)" % (self.elem_type, self.value)


class Compound(dict):
    tag_id = TAG_COMPOUND

    @property
    def value(self):
        return self


def unwrap(obj):
    """Convert Tag tree to plain Python primitives for inspection."""
    if isinstance(obj, Compound):
        return {k: unwrap(v) for k, v in obj.items()}
    if isinstance(obj, List):
        return [unwrap(v) for v in obj.value]
    if isinstance(obj, Tag):
        return obj.value
    return obj


def _read_exact(buf, n):
    data = buf.read(n)
    if len(data) != n:
        raise EOFError("Expected %d bytes, got %d" % (n, len(data)))
    return data


def _read_str(buf):
    ln = struct.unpack(">H", _read_exact(buf, 2))[0]
    return _read_exact(buf, ln).decode("utf-8", errors="replace")


def _write_str(buf, s):
    raw = s.encode("utf-8")
    buf.write(struct.pack(">H", len(raw)))
    buf.write(raw)


def _read_payload(buf, tag_id):
    if tag_id == TAG_BYTE:
        return Byte(struct.unpack(">b", _read_exact(buf, 1))[0])
    if tag_id == TAG_SHORT:
        return Short(struct.unpack(">h", _read_exact(buf, 2))[0])
    if tag_id == TAG_INT:
        return Int(struct.unpack(">i", _read_exact(buf, 4))[0])
    if tag_id == TAG_LONG:
        return Long(struct.unpack(">q", _read_exact(buf, 8))[0])
    if tag_id == TAG_FLOAT:
        return Float(struct.unpack(">f", _read_exact(buf, 4))[0])
    if tag_id == TAG_DOUBLE:
        return Double(struct.unpack(">d", _read_exact(buf, 8))[0])
    if tag_id == TAG_BYTE_ARRAY:
        ln = struct.unpack(">i", _read_exact(buf, 4))[0]
        return ByteArray(list(struct.unpack(">%db" % ln, _read_exact(buf, ln))))
    if tag_id == TAG_STRING:
        return String(_read_str(buf))
    if tag_id == TAG_LIST:
        elem_type = struct.unpack(">B", _read_exact(buf, 1))[0]
        ln = struct.unpack(">i", _read_exact(buf, 4))[0]
        items = [_read_payload(buf, elem_type) for _ in range(ln)]
        return List(elem_type, items)
    if tag_id == TAG_COMPOUND:
        out = Compound()
        while True:
            tid = struct.unpack(">B", _read_exact(buf, 1))[0]
            if tid == TAG_END:
                break
            name = _read_str(buf)
            out[name] = _read_payload(buf, tid)
        return out
    if tag_id == TAG_INT_ARRAY:
        ln = struct.unpack(">i", _read_exact(buf, 4))[0]
        return IntArray(list(struct.unpack(">%di" % ln, _read_exact(buf, ln * 4))))
    if tag_id == TAG_LONG_ARRAY:
        ln = struct.unpack(">i", _read_exact(buf, 4))[0]
        return LongArray(list(struct.unpack(">%dq" % ln, _read_exact(buf, ln * 8))))
    raise ValueError("Unknown NBT tag id: %d" % tag_id)


def _write_payload(buf, tag):
    tid = tag.tag_id
    if tid == TAG_BYTE:
        buf.write(struct.pack(">b", tag.value))
    elif tid == TAG_SHORT:
        buf.write(struct.pack(">h", tag.value))
    elif tid == TAG_INT:
        buf.write(struct.pack(">i", tag.value))
    elif tid == TAG_LONG:
        buf.write(struct.pack(">q", tag.value))
    elif tid == TAG_FLOAT:
        buf.write(struct.pack(">f", tag.value))
    elif tid == TAG_DOUBLE:
        buf.write(struct.pack(">d", tag.value))
    elif tid == TAG_BYTE_ARRAY:
        buf.write(struct.pack(">i", len(tag.value)))
        if tag.value:
            buf.write(struct.pack(">%db" % len(tag.value), *tag.value))
    elif tid == TAG_STRING:
        _write_str(buf, tag.value)
    elif tid == TAG_LIST:
        elem_type = tag.elem_type if tag.value else (tag.elem_type or TAG_END)
        buf.write(struct.pack(">Bi", elem_type, len(tag.value)))
        for item in tag.value:
            _write_payload(buf, item)
    elif tid == TAG_COMPOUND:
        for k, v in tag.items():
            buf.write(struct.pack(">B", v.tag_id))
            _write_str(buf, k)
            _write_payload(buf, v)
        buf.write(b"\x00")
    elif tid == TAG_INT_ARRAY:
        buf.write(struct.pack(">i", len(tag.value)))
        if tag.value:
            buf.write(struct.pack(">%di" % len(tag.value), *tag.value))
    elif tid == TAG_LONG_ARRAY:
        buf.write(struct.pack(">i", len(tag.value)))
        if tag.value:
            buf.write(struct.pack(">%dq" % len(tag.value), *tag.value))
    else:
        raise ValueError("Unsupported tag: %r" % (tag,))


def loads(raw):
    if len(raw) >= 2 and raw[0] == 0x1F and raw[1] == 0x8B:
        raw = gzip.decompress(raw)
    buf = io.BytesIO(raw)
    tid = struct.unpack(">B", _read_exact(buf, 1))[0]
    if tid != TAG_COMPOUND:
        raise ValueError("Root NBT tag must be Compound, got %d" % tid)
    _name = _read_str(buf)
    return _read_payload(buf, tid)


def dumps(root, compress=True):
    buf = io.BytesIO()
    buf.write(struct.pack(">B", TAG_COMPOUND))
    _write_str(buf, "")
    _write_payload(buf, root)
    raw = buf.getvalue()
    if compress:
        # Use mtime=0 for deterministic output across runs
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as gz:
            gz.write(raw)
        return out.getvalue()
    return raw


def read_file(path):
    with open(path, "rb") as fh:
        return loads(fh.read())


def write_file(path, root, compress=True):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(dumps(root, compress=compress))


# ---------------------------------------------------------------------------
# Anvil (.mca) region & chunk block reading (1.18+ / 1.21.11 format)
# ---------------------------------------------------------------------------

def iter_region_chunks(mca_path):
    """Yield (chunk_x, chunk_z, chunk_nbt) for all populated chunks in an .mca file."""
    with open(mca_path, "rb") as fh:
        data = fh.read()
    if len(data) < 8192:
        return
    for idx in range(1024):
        loc = struct.unpack_from(">I", data, idx * 4)[0]
        if loc == 0:
            continue
        sector_offset = (loc >> 8) * 4096
        sector_count = loc & 0xFF
        if sector_offset == 0 or sector_count == 0 or sector_offset + 5 > len(data):
            continue
        length, comp = struct.unpack_from(">IB", data, sector_offset)
        payload = data[sector_offset + 5: sector_offset + 4 + length]
        if comp == 1:
            raw = gzip.decompress(payload)
        elif comp == 2:
            raw = zlib.decompress(payload)
        elif comp == 3:
            raw = payload
        else:
            continue
        chunk = loads(raw)
        cx = chunk["xPos"].value
        cz = chunk["zPos"].value
        yield cx, cz, chunk


class WorldReader:
    """Lazy reader over a world's region/ directory."""

    def __init__(self, region_dir):
        self.region_dir = region_dir
        self._regions = {}   # (rx, rz) -> {(cx, cz): chunk_nbt}
        self._decoded = {}   # (cx, cz) -> (sections_dict, block_entities_dict)

    def _load_region(self, rx, rz):
        key = (rx, rz)
        if key in self._regions:
            return self._regions[key]
        path = os.path.join(self.region_dir, "r.%d.%d.mca" % (rx, rz))
        chunks = {}
        if os.path.isfile(path):
            for cx, cz, chunk in iter_region_chunks(path):
                chunks[(cx, cz)] = chunk
        self._regions[key] = chunks
        return chunks

    def get_chunk(self, cx, cz):
        rx, rz = cx >> 5, cz >> 5
        return self._load_region(rx, rz).get((cx, cz))

    def _decode_chunk(self, cx, cz):
        key = (cx, cz)
        if key in self._decoded:
            return self._decoded[key]
        chunk = self.get_chunk(cx, cz)
        if chunk is None:
            self._decoded[key] = ({}, {})
            return self._decoded[key]

        sections = {}
        for sec in chunk.get("sections", []):
            sy = sec["Y"].value
            bs = sec.get("block_states")
            if not bs:
                continue
            pal = bs.get("palette")
            if not pal:
                continue
            pal_list = []
            for entry in pal:
                name = entry["Name"].value
                props = {}
                if "Properties" in entry:
                    for pk, pv in entry["Properties"].items():
                        props[pk] = pv.value
                pal_list.append((name, props))
            if len(pal_list) == 1 or "data" not in bs:
                sections[sy] = (pal_list, None, 0)
            else:
                bits = max(4, (len(pal_list) - 1).bit_length())
                longs = [v & 0xFFFFFFFFFFFFFFFF for v in bs["data"].value]
                sections[sy] = (pal_list, longs, bits)

        bes = {}
        for be in chunk.get("block_entities", []):
            bx, by, bz = be["x"].value, be["y"].value, be["z"].value
            bes[(bx, by, bz)] = be

        self._decoded[key] = (sections, bes)
        return self._decoded[key]

    def get_block(self, x, y, z):
        """Return (block_name, properties_dict, block_entity_compound_or_None)."""
        cx, cz = x >> 4, z >> 4
        sections, bes = self._decode_chunk(cx, cz)
        sy = y >> 4
        sec = sections.get(sy)
        if sec is None:
            return ("minecraft:air", {}, None)
        pal_list, longs, bits = sec
        if longs is None:
            name, props = pal_list[0]
        else:
            lx, ly, lz = x & 15, y & 15, z & 15
            idx = (ly << 8) | (lz << 4) | lx
            per_long = 64 // bits
            long_idx = idx // per_long
            bit_off = (idx % per_long) * bits
            mask = (1 << bits) - 1
            pal_idx = (longs[long_idx] >> bit_off) & mask
            name, props = pal_list[pal_idx]
        return (name, dict(props), bes.get((x, y, z)))
