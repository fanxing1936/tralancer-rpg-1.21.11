# -*- coding: utf-8 -*-
"""地形配方（terrain_dsl 的双后端：B = JsonB(g) 进游戏，B = NumpyB(x, z) 离线求值）。

配方里只能出现噪声（含按二维噪声扭曲），不能出现坐标还原 x/z —— 这样才能：
  1. 在偏移位置重算一遍（shift），用差分求坡度；
  2. 不增加 NoiseChunk 展开成本（见 overworld_world.terrain 顶部的注释）。

学的是 World Machine 官方示例的导出高度图（只做统计与目视对比，不解析 .tmd，不进包）：
  ridgy_mountains / coastal_mtn2：树枝状分叉的锋利山脊 + 平缓的沉积谷底；频谱斜率约 -4，脊尖谷圆（拉普拉斯偏度为负）。
"""
from terrain_dsl import q

# 高山高度（格，相对内陆基准 ≈ 海平面 +6）：主体峰顶约 y 300，少数孤峰更高（用户 2026-11-26）
ALP_BASE, ALP_RIDGE, ALP_PEAK = 25.0, 200.0, 230.0


def _ridged(B, N, name, first, amps, xz, warp, width):
    """锐化的山脊场 0..1：|n| 越小越高，width 为脊宽（|n| 的分位数）。"""
    return B.lin(B.abs(N(name, first, amps, xz, warp)), [(0.0, 1.0), (q(50 + width * 0.25), 0.82), (q(50 + width * 0.6), 0.35), (q(50 + width), 0.0)])


def alpine_M(B, wx, wz, shift=(0.0, 0.0)):
    """高山山体（格，乘 alp² 之前）：脊状多重分形（Musgrave）。
    每阶脊信号 s_k ≈ (1 - 2|n_k|)²（用平滑样条，免得钳位出折痕），权重 w_k = clamp(2·s_{k-1})——细节只长在上一阶的高处，顺着脊分叉，
    这就是参考图里树枝状、脊顶粗糙的山体；最后把最低的一段压缓，成冲积谷地。"""
    N = lambda name, first, amps, xz, warp=None: B.noise(name, first, amps, xz, warp=warp, shift=shift)
    OCT = [("ridge", -9, 0.8, (110.0, wx, wz), 1.0), ("branch", -8, 0.85, (60.0, wz, wx), 0.55),
           ("spur", -7, 0.9, (30.0, wx, wz), 0.32), ("spur2", -6, 0.95, (14.0, wz, wx), 0.18), ("spur3", -5, 1.0, None, 0.1)]
    h, w = 0.0, 1.0
    for k, (name, first, xz, warp, amp) in enumerate(OCT):
        s = B.lin(B.abs(N(name, first, [1.0], xz, warp)), [(0.0, 1.0), (0.08, 0.72), (0.2, 0.36), (0.36, 0.1), (0.55, 0.0)])   # ≈(1-2|n|)²，但没有折痕
        if k: s = B.mul(s, w)
        h = s if k == 0 else B.add(h, B.mul(amp, s))
        w = B.clamp(B.mul(2.2, s), 0.0, 1.0)
    prov = B.lin(N("alp_prov", -9, [1.0, 0.55, 0.3], 1.0), [(q(10), 0.0), (q(90), 1.0)])
    h = B.mul(h, B.add(0.45, B.mul(0.55, prov)))             # 0..约 2
    h = B.lin(h, [(0.0, 0.0), (0.15, 0.03), (0.4, 0.16), (0.8, 0.45), (1.3, 0.85), (2.0, 1.25)])
    peak = B.lin(N("peak", -8, [1.0, 0.6], 0.9), [(q(93), 0.0), (q(98.5), 0.85), (q(99.8), 1.0)])
    return B.add(ALP_BASE, B.mul(ALP_RIDGE, h), B.mul(ALP_PEAK, peak, h), B.mul(25.0, prov))


# 坡度分档（用户 2026-11-26）：>70° 方解石，>50° 岩石（石头+原石），>20° 青色陶瓦。比较的是坡度平方 |∇h|²
TAN2 = {20: 0.3640 ** 2, 50: 1.1918 ** 2, 70: 2.7475 ** 2}
D = 2.0      # 中心差分的半步（格）


def slope2(B, M_at, scale):
    """|∇h|²，h = scale·M。M_at(shift) 在偏移处求 M；scale 为乘在 M 外面的系数（如 alp²）。"""
    gx = B.mul(1.0 / (2 * D), B.add(M_at((D, 0.0)), B.mul(-1.0, M_at((-D, 0.0)))))
    gz = B.mul(1.0 / (2 * D), B.add(M_at((0.0, D)), B.mul(-1.0, M_at((0.0, -D)))))
    return B.mul(B.square(scale), B.add(B.square(gx), B.square(gz)))
