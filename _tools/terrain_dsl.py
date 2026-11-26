# -*- coding: utf-8 -*-
"""地形配方的双后端：同一份配方既能输出密度函数 JSON（游戏用），也能用 numpy 离线求值（调参、和参考图对比用）。

只用游戏密度函数做得到的运算：noise、shifted_noise（位移=其它二维函数×常数）、add、mul、abs、square、min、max、
clamp、spline（三次 Hermite，端点外按端点导数线性外推）。没有侵蚀模拟、没有 Worley——侵蚀感全靠这些拼出来。

numpy 后端的噪声：仿 1.21 的 NormalNoise（两套改进 Perlin 八度叠加、第二套坐标 ×1.0181268882175227、
按八度数归一）。种子不同，数值不会和游戏逐点相同，但分布（标准差约 0.28）、频谱和尺度一致——调参看的就是这些。
"""
import math
import numpy as np

SPLINE_K = 1.0181268882175227


# ------------------------------------------------------------------ numpy：改进 Perlin（2D 截面，y=0）
class _Perlin:
    def __init__(self, rng):
        self.p = np.concatenate([rng.permutation(256)] * 2)
        self.o = rng.random(3) * 256.0

    @staticmethod
    def _fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    _G = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
                   [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1], [1, 1, 0], [0, -1, 1], [-1, 1, 0], [0, -1, -1]], float)

    def __call__(self, x, z):
        x = x + self.o[0]; y = np.zeros_like(x) + self.o[1]; z = z + self.o[2]
        xi, yi, zi = np.floor(x), np.floor(y), np.floor(z)
        xf, yf, zf = x - xi, y - yi, z - zi
        X, Y, Z = xi.astype(np.int64) & 255, yi.astype(np.int64) & 255, zi.astype(np.int64) & 255
        p = self.p
        def g(h, dx, dy, dz):
            gv = self._G[h & 15]
            return gv[..., 0] * dx + gv[..., 1] * dy + gv[..., 2] * dz
        A = p[X] + Y; AA = p[A] + Z; AB = p[A + 1] + Z; B = p[X + 1] + Y; BA = p[B] + Z; BB = p[B + 1] + Z
        u, v, w = self._fade(xf), self._fade(yf), self._fade(zf)
        l = lambda a, b, t: a + t * (b - a)
        return l(l(l(g(p[AA], xf, yf, zf), g(p[BA], xf - 1, yf, zf), u), l(g(p[AB], xf, yf - 1, zf), g(p[BB], xf - 1, yf - 1, zf), u), v),
                 l(l(g(p[AA + 1], xf, yf, zf - 1), g(p[BA + 1], xf - 1, yf, zf - 1), u), l(g(p[AB + 1], xf, yf - 1, zf - 1), g(p[BB + 1], xf - 1, yf - 1, zf - 1), u), v), w)


class _NormalNoise:
    def __init__(self, seed, first, amps):
        rng = np.random.default_rng(seed)
        self.first, self.amps = first, list(amps)
        n = len(amps)
        self.a = [_Perlin(rng) if a else None for a in amps]
        self.b = [_Perlin(rng) if a else None for a in amps]
        lo = 2.0 ** (n - 1) / (2.0 ** n - 1)
        self.w = [a * lo * 0.5 ** i for i, a in enumerate(amps)]
        nz = [i for i, a in enumerate(amps) if a]
        span = (nz[-1] - nz[0]) if nz else 0
        self.vf = (1.0 / 6.0) / (0.1 * (1.0 + 1.0 / (span + 1)))

    def __call__(self, x, z):
        out = 0.0
        for i, (pa, pb, w) in enumerate(zip(self.a, self.b, self.w)):
            if pa is None: continue
            f = 2.0 ** (self.first + i)
            out = out + w * (pa(x * f, z * f) + pb(x * f * SPLINE_K, z * f * SPLINE_K))
        return out * self.vf


# ------------------------------------------------------------------ 三次 Hermite 样条（与游戏 CubicSpline 一致）
def spline_eval(c, pts):
    """pts: [(location, value, derivative)]"""
    xs = np.array([p[0] for p in pts], float); ys = np.array([p[1] for p in pts], float); ds = np.array([p[2] for p in pts], float)
    out = np.empty_like(c, dtype=float)
    lo, hi = c < xs[0], c > xs[-1]
    out[lo] = ys[0] + ds[0] * (c[lo] - xs[0])
    out[hi] = ys[-1] + ds[-1] * (c[hi] - xs[-1])
    mid = ~(lo | hi)
    cm = c[mid]
    i = np.clip(np.searchsorted(xs, cm, side="right") - 1, 0, len(xs) - 2)
    x0, x1, y0, y1, d0, d1 = xs[i], xs[i + 1], ys[i], ys[i + 1], ds[i], ds[i + 1]
    dx = x1 - x0
    t = (cm - x0) / dx
    a = d0 * dx - (y1 - y0); b = -d1 * dx + (y1 - y0)
    out[mid] = (y0 + t * (y1 - y0)) + t * (1 - t) * (a + t * (b - a))
    return out


def lin_pts(pts):
    """折线点 → 带斜率的样条点：中间点斜率取两侧平均，端点 0（与 overworld_world.lin 相同）。"""
    out = []
    for i, (x, v) in enumerate(pts):
        s = (pts[i + 1][1] - pts[i - 1][1]) / (pts[i + 1][0] - pts[i - 1][0]) if 0 < i < len(pts) - 1 else 0.0
        out.append((float(x), float(v), float(s)))
    return out


# ------------------------------------------------------------------ 后端
class NumpyB:
    """离线求值。x、z 为格坐标数组（二维）。"""
    def __init__(self, x, z, seed=1):
        self.x, self.z, self.seed, self._nz = x, z, seed, {}

    def _noise(self, name, first, amps):
        k = (name, first, tuple(amps))
        if k not in self._nz:
            self._nz[k] = _NormalNoise((hash(name) & 0xffffffff) ^ self.seed, first, amps)
        return self._nz[k]

    # 噪声：xz 为 xz_scale；warp 为 (amp, wx, wz)：在 (x + amp·wx, z + amp·wz) 取样（格）
    def noise(self, name, first, amps, xz=1.0, warp=None, shift=(0.0, 0.0)):
        n = self._noise(name, first, amps)
        X, Z = self.x * xz, self.z * xz
        if warp:
            amp, wx, wz = warp
            X = X + amp * xz * wx; Z = Z + amp * xz * wz
        return n(X + shift[0] * xz, Z + shift[1] * xz)

    def c(self, v): return np.full_like(self.x, float(v), dtype=float)
    def add(self, *a): return sum(self._v(v) for v in a)
    def mul(self, *a):
        out = 1.0
        for v in a: out = out * self._v(v)
        return out
    def abs(self, a): return np.abs(a)
    def square(self, a): return a * a
    def mn(self, a, b): return np.minimum(self._v(a), self._v(b))
    def mx(self, a, b): return np.maximum(self._v(a), self._v(b))
    def clamp(self, a, lo, hi): return np.clip(a, lo, hi)
    def spline(self, c, pts): return spline_eval(self._v(c), [(p[0], p[1], p[2] if len(p) > 2 else 0.0) for p in pts])
    def lin(self, c, pts): return spline_eval(self._v(c), lin_pts(pts))
    def ref(self, name, v): return v          # 游戏里是具名引用（flat_cache）；离线直接用值
    def _v(self, v): return self.c(v) if isinstance(v, (int, float)) else v


class JsonB:
    """输出密度函数 JSON。g 为 overworld_world.Gen；噪声定义写进 rpg:ow/。"""
    def __init__(self, g):
        import overworld_world as OW
        self.g, self.OW = g, OW

    def noise(self, name, first, amps, xz=1.0, warp=None, shift=(0.0, 0.0)):
        n = self.g.nz(name, first, amps)
        if warp:
            amp, wx, wz = warp
            if shift == (0.0, 0.0):
                return self.g.warped(n, xz, amp, wx, wz)
            OW = self.OW
            return {"type": "minecraft:shifted_noise", "noise": n, "xz_scale": xz * self.g.sc, "y_scale": 0.0,
                    "shift_x": OW.add(OW.mul(amp * xz, wx), shift[0] * xz), "shift_y": 0.0,
                    "shift_z": OW.add(OW.mul(amp * xz, wz), shift[1] * xz)}
        if shift != (0.0, 0.0):
            s = xz * self.g.sc
            return {"type": "minecraft:shifted_noise", "noise": n, "xz_scale": s, "y_scale": 0.0,
                    "shift_x": shift[0] * xz, "shift_y": 0.0, "shift_z": shift[1] * xz}
        return self.g.noise(n, xz)

    def c(self, v): return float(v)
    def add(self, *a): return self.OW.add(*a)
    def mul(self, *a): return self.OW.mul(*a)
    def abs(self, a): return self.OW.un("abs", a)
    def square(self, a): return self.OW.un("square", a)
    def mn(self, a, b): return self.OW.mn(a, b)
    def mx(self, a, b): return self.OW.mx(a, b)
    def clamp(self, a, lo, hi): return self.OW.clamp(a, lo, hi)
    def spline(self, c, pts): return self.OW.spline(c, pts)
    def lin(self, c, pts): return self.OW.lin(c, pts)
    def ref(self, name, v): return self.g.df(name, self.OW.fc(v))


def q(p, sd=0.28):
    from statistics import NormalDist
    return NormalDist().inv_cdf(p / 100.0) * sd
