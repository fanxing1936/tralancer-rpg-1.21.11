# -*- coding: utf-8 -*-
"""Tiny pure-python PNG reader/writer -- enough to measure and rescale item art."""

import struct
import zlib


def _unfilter(raw, w, h, bpp, stride=None):
    out = bytearray()
    if stride is None:
        stride = w * bpp
    prev = bytearray(stride)
    i = 0
    for _ in range(h):
        ft = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if ft == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 0xFF
        elif ft == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif ft == 3:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif ft == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        elif ft != 0:
            raise ValueError("filter %d" % ft)
        out += line
        prev = line
    return bytes(out)


def read(path):
    """-> (width, height, rgba bytes)."""
    return decode(open(path, "rb").read(), path)


def decode(d, path="<bytes>"):
    """Same as read(), but from an in-memory PNG (e.g. straight out of a jar)."""
    assert d[:8] == b"\x89PNG\r\n\x1a\n", path
    i = 8
    idat = b""
    pal = None
    trns = None
    w = h = depth = ctype = None
    while i < len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        typ = d[i + 4:i + 8]
        body = d[i + 8:i + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", body[:10])
        elif typ == b"PLTE":
            pal = body
        elif typ == b"tRNS":
            trns = body
        elif typ == b"IDAT":
            idat += body
        elif typ == b"IEND":
            break
        i += 12 + ln
    if depth not in (1, 2, 4, 8):
        raise ValueError("unsupported bit depth (%s is %d-bit)" % (path, depth))
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    if depth == 8:
        raw = _unfilter(zlib.decompress(idat), w, h, channels)
    else:
        # Sub-byte depths: filtering still works on whole bytes, with a
        # ceil()'d scanline and a minimum one-byte filter step.  Expand the
        # packed samples to one byte each afterwards -- greyscale is rescaled
        # to full range, palette indices are kept as-is.
        bits = channels * depth
        stride = (w * bits + 7) // 8
        packed = _unfilter(zlib.decompress(idat), w, h, max(1, bits // 8), stride)
        mask = (1 << depth) - 1
        scale = 255 // mask
        raw = bytearray(w * h * channels)
        for y in range(h):
            base = y * stride
            for x in range(w * channels):
                bit = x * depth
                byte = packed[base + (bit >> 3)]
                v = (byte >> (8 - depth - (bit & 7))) & mask
                raw[y * w * channels + x] = v if ctype == 3 else v * scale

    # For greyscale and truecolour, tRNS is not an alpha table but a single
    # fully-transparent colour key.  Several vanilla item sprites are stored
    # that way (grey + tRNS); ignoring it makes them decode fully opaque, which
    # turns a helmet into a filled square and hides whatever it is drawn over.
    key_grey = key_rgb = None
    if trns:
        if ctype == 0:
            v = struct.unpack(">H", trns[:2])[0]
            # samples were rescaled to full range above, so rescale the key too
            key_grey = v if depth == 8 else v * (255 // ((1 << depth) - 1))
        elif ctype == 2:
            key_rgb = tuple(struct.unpack(">HHH", trns[:6]))

    rgba = bytearray(w * h * 4)
    for p in range(w * h):
        s = p * channels
        if ctype == 6:
            rgba[p * 4:p * 4 + 4] = raw[s:s + 4]
        elif ctype == 2:
            rgba[p * 4:p * 4 + 3] = raw[s:s + 3]
            rgba[p * 4 + 3] = 0 if (key_rgb and tuple(raw[s:s + 3]) == key_rgb) else 255
        elif ctype == 3:
            idx = raw[s]
            rgba[p * 4:p * 4 + 3] = pal[idx * 3:idx * 3 + 3]
            rgba[p * 4 + 3] = trns[idx] if trns and idx < len(trns) else 255
        elif ctype == 0:
            v = raw[s]
            rgba[p * 4:p * 4 + 3] = bytes((v, v, v))
            rgba[p * 4 + 3] = 0 if v == key_grey else 255
        elif ctype == 4:
            v = raw[s]
            rgba[p * 4:p * 4 + 3] = bytes((v, v, v))
            rgba[p * 4 + 3] = raw[s + 1]
    return w, h, bytes(rgba)


def write(path, w, h, rgba):
    open(path, "wb").write(encode(w, h, rgba))


def encode(w, h, rgba):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += rgba[y * w * 4:(y + 1) * w * 4]

    def chunk(typ, body):
        return (struct.pack(">I", len(body)) + typ + body
                + struct.pack(">I", zlib.crc32(typ + body) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def bbox(w, h, rgba, alpha_min=1):
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            if rgba[(y * w + x) * 4 + 3] >= alpha_min:
                if x < x0: x0 = x
                if y < y0: y0 = y
                if x > x1: x1 = x
                if y > y1: y1 = y
    if x1 < 0:
        return None
    return x0, y0, x1, y1


def nearest(w, h, rgba, nw, nh):
    out = bytearray(nw * nh * 4)
    for y in range(nh):
        sy = min(h - 1, y * h // nh)
        for x in range(nw):
            sx = min(w - 1, x * w // nw)
            s = (sy * w + sx) * 4
            out[(y * nw + x) * 4:(y * nw + x) * 4 + 4] = rgba[s:s + 4]
    return bytes(out)


def paste_fit(w, h, rgba, canvas, box):
    """Scale the art so its bounding box fills `box` fraction of a square canvas."""
    bb = bbox(w, h, rgba)
    if bb is None:
        return nearest(w, h, rgba, canvas, canvas)
    x0, y0, x1, y1 = bb
    aw, ah = x1 - x0 + 1, y1 - y0 + 1
    target = int(round(canvas * box))
    scale = min(target / float(aw), target / float(ah))
    nw, nh = max(1, int(round(aw * scale))), max(1, int(round(ah * scale)))

    art = bytearray(aw * ah * 4)
    for y in range(ah):
        s = ((y0 + y) * w + x0) * 4
        art[y * aw * 4:(y + 1) * aw * 4] = rgba[s:s + aw * 4]
    small = nearest(aw, ah, bytes(art), nw, nh)

    out = bytearray(canvas * canvas * 4)
    ox, oy = (canvas - nw) // 2, (canvas - nh) // 2
    for y in range(nh):
        d = ((oy + y) * canvas + ox) * 4
        out[d:d + nw * 4] = small[y * nw * 4:(y + 1) * nw * 4]
    return bytes(out)
