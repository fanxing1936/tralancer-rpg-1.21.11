# -*- coding: utf-8 -*-
"""序章的五段过场（脚本书 场 1、3、4、6、7）：展示实体演员 + 旁观镜头 + 双语字幕。

镜头（2026-11-22 技术验证）：玩家切旁观、spectate 一个空的 item_display「机位」，机位用带 teleport_duration 的传送
平滑移动（位置和朝向都会插值，最长 59 刻）；换镜头就是 teleport_duration 设 0 再传送。
演员是不带 AI 的卫道士载体套序章专用模型（rpg:prologue_<名字>，add_prologue_models.py）；路西法在场 6 被占据时
换图集（look/possessed），之后一直保持。
动画是 rpg:<模型>/anim/enter/<动作>（as 载体）。

坐标都在 rpg:armageddon 里，以场地中心 (0, 81, 0) 为准：石台半径 4，深坑底 y=41。
"""
DIM = "rpg:armageddon"

# 演员 → 外观函数前缀。序章专用模型（add_prologue_models.py，Codex 交付），载体带 rpg.pr.w.<名字>，召唤后立刻换装。
ACTORS = {k: "rpg:prologue_" + k for k in ("lucifer", "michael", "beelzebub", "belial", "mammon")}
# 脚本书里的动画名都已经是模型里的同名动作；这里只放需要改名的
CLIP = {}
YAW_E, YAW_W, YAW_S, YAW_N = -90, 90, 0, 180


CAM_DUR = "data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value "
CAM_TP = "run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] "
CAM_DUR_RAW = CAM_DUR + "%d"


class Cut:
    """auto_cam=True：场景里写的 cam/camlook 不直接下发，而是记成镜头关键点，最后由 smooth_cams() 改写成连续运镜
    （用户 2026-11-22：滑一段就停住、干等到下个镜头，看着像卡住）。规则：硬切（插值 0）开一个新镜头；
    镜头里的滑动目标点按到达时刻串成路径，最后一段拉长到下个硬切为止；完全不动的镜头沿视线方向轻轻推近。"""

    def __init__(self, name, auto_cam=False):
        self.name = name
        self.beats = {}
        self.auto_cam = auto_cam
        self.cams = []          # (刻, 插值刻数, [x, y, z, yaw, pitch])
        self._dur = 0
        self.track = {}         # 刻 → 机位传送（campath 每刻一条，单独分派，不占 beat 文件）

    def at(self, sec, *cmds):
        t = int(round(sec * 20))
        keep = []
        for c in cmds:
            if self.auto_cam and c.startswith(CAM_DUR):
                self._dur = int(c[len(CAM_DUR):])
                continue
            if self.auto_cam and CAM_TP in c:
                self.cams.append((t, self._dur, [float(v) for v in c.split(CAM_TP)[1].split()]))
                continue
            keep.append(c)
        self.beats.setdefault(t, []).extend(keep)
        return self

    def smooth_cams(self):
        if not self.auto_cam or not self.cams:
            return
        import math
        end = self.end_tick()
        ev = sorted(self.cams, key=lambda e: e[0])
        cuts = [i for i, e in enumerate(ev) if e[1] == 0]
        if not cuts or cuts[0] != 0:
            raise ValueError("%s: 自动运镜的第一个镜头必须是硬切" % self.name)
        self.auto_cam = False
        for n, i in enumerate(cuts):
            t0, _, p0 = ev[i]
            t1 = ev[cuts[n + 1]][0] if n + 1 < len(cuts) else end
            if t1 - t0 < 2:
                self.at(t0 / 20.0, *cam(*p0))
                continue
            keys = [(t0, p0)]
            for tk, d, p in ev[i + 1:(cuts[n + 1] if n + 1 < len(cuts) else len(ev))]:
                keys.append((max(tk + d, keys[-1][0] + 1), p))
            if len(keys) == 1:          # 静止镜头：沿视线推近一点（每秒 0.25 格，最多 0.6 格）
                yaw, pitch = math.radians(p0[3]), math.radians(p0[4])
                k = min(0.25 * (t1 - t0) / 20.0, 0.6)
                fwd = (-math.sin(yaw) * math.cos(pitch), -math.sin(pitch), math.cos(yaw) * math.cos(pitch))
                keys.append((t1 - 1, [p0[0] + fwd[0] * k, p0[1] + fwd[1] * k, p0[2] + fwd[2] * k, p0[3], p0[4]]))
            else:
                # 超过下个硬切的关键点按时间截断；最后一个关键点拉到镜头结束，路上不停
                kept = [keys[0]]
                for (ta, pa), (tb, pb) in zip(keys, keys[1:]):
                    if tb <= t1 - 1:
                        kept.append((tb, pb))
                    else:
                        u = (t1 - 1 - ta) / float(tb - ta)
                        pb = [a + (b - a) * u for a, b in zip(pa, pb)]
                        kept.append((t1 - 1, pb))
                        break
                keys = kept
                if keys[-1][0] < t1 - 1:
                    keys[-1] = (t1 - 1, keys[-1][1])
            campath(self, [(tk / 20.0,) + tuple(p) for tk, p in keys])

    def end_tick(self):
        return max(self.beats) if self.beats else 0


# 空间裂缝：场地北侧很大的一块（贴图 14×17 格，中心离地 6.5 格）
RIFT = (0, 87.5, -9)
# 石台下的大洞穴：地面 y=34（路西法落到 35）
FLOOR = 35


def camlook(x, y, z, tx, ty, tz, dur=0):
    """机位在 (x, y, z)，看向 (tx, ty, tz)。"""
    import math
    dx, dy, dz = tx - x, ty - y, tz - z
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return cam(x, y, z, round(yaw, 1), round(pitch, 1), dur)


def vfx(cmds, x, y, z):
    """地下城特效（米迦勒那套 rpg:michael_vfx，michael_boss_lib 的现成组合），放在 (x, y, z)。"""
    return ["execute in %s positioned %g %g %g run %s" % (DIM, x, y, z, c) for c in cmds]


def L():
    import michael_boss_lib
    return michael_boss_lib


def wisp(cut, who, sec, frm, colour, part):
    """领主化作一缕烟，飞奔进裂缝：先起跳（flee），0.6 秒后身体散成烟团，烟团 12 刻冲进裂缝。"""
    x, y, z = frm
    cut.at(sec, *anim(who, "flee"))
    t = sec + 0.6
    cut.at(t, *drop_actor(who), *vfx(L().smoke_puff(size=3.0), x, y + 0.6, z),
           *P("minecraft:large_smoke", x, y + 1, z, 0.5, 0.8, 0.5, 0.02, 30),
           *P(part, x, y + 1, z, 0.6, 1, 0.6, 0, 40),
           *["execute in %s run summon minecraft:item_display %g %g %g {Tags:[\"rpg.pr.wisp\",\"rpg.pr.ent\"],billboard:\"center\","
             "teleport_duration:1,brightness:{sky:15,block:15},item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":"
             "\"rpg:prologue_fx/smoke_0\"}},item_display:\"fixed\",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],"
             "translation:[0f,0f,0f],scale:[3.4f,3.4f,3.4f]}}" % (DIM, x, y + 1.2, z)],
           *snd("minecraft:entity.phantom.flap", 1.2, 0.6), *snd("minecraft:entity.breeze.whirl", 1, 0.7))
    n = 12
    for i in range(1, n + 1):
        f = i / float(n)
        f = f * f * (3 - 2 * f)
        px, py, pz = x + (RIFT[0] - x) * f, y + 1.2 + (RIFT[1] - y - 1.2) * f + 1.5 * (1 - (2 * f - 1) ** 2), z + (RIFT[2] - z) * f
        cut.at(t + i / 20.0, "execute in %s run tp @e[type=minecraft:item_display,tag=rpg.pr.wisp] %g %g %g" % (DIM, px, py, pz),
               *P("minecraft:dust{color:%s,scale:2.2}" % colour, px, py, pz, 0.3, 0.3, 0.3, 0, 8),
               *P("minecraft:large_smoke", px, py, pz, 0.2, 0.2, 0.2, 0.01, 3))
    cut.at(t + (n + 1) / 20.0, "kill @e[type=minecraft:item_display,tag=rpg.pr.wisp]",
           *vfx(L().impact(size=3.0), *RIFT), *P("minecraft:reverse_portal", RIFT[0], RIFT[1], RIFT[2], 1.5, 2, 0.3, 0.3, 120),
           *P(part, RIFT[0], RIFT[1], RIFT[2], 1, 1.5, 0.3, 0, 40), *snd("minecraft:entity.enderman.teleport", 1.2, 0.6))


def _num(v, d):
    """坐标一律带小数点：tp 的整数 x/z 会被当成方块中心自动加 0.5，镜头路过整数点会跳一下。"""
    s = ("%.*f" % (d, v)).rstrip("0")
    s = s + "0" if s.endswith(".") else s
    return "0.0" if s == "-0.0" else s


def cam(x, y, z, yaw, pitch, dur=0):
    return ["data modify entity @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] teleport_duration set value %d" % min(dur, 59),
            "execute in %s run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] %s %s %s %s %s"
            % (DIM, _num(x, 3), _num(y, 3), _num(z, 3), _num(yaw, 2), _num(pitch, 2))]


CAM_LAG = 3     # 机位每刻传送一次、插值 3 刻：客户端一直在追最新的点，速度连续；漏一两个包也不会停顿


def _mono_tangents(ts, vs):
    """单调三次 Hermite（Fritsch–Carlson）的切线：过关键点时速度连续，又不会冲过头（镜头不会甩进墙里）。
    两端用相邻一段的斜率，镜头到镜头结束都还在动。"""
    n = len(ts)
    d = [(vs[i + 1] - vs[i]) / (ts[i + 1] - ts[i]) for i in range(n - 1)]
    m = [d[0]] + [0.0] * (n - 2) + [d[-1]]
    for i in range(1, n - 1):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            h0, h1 = ts[i] - ts[i - 1], ts[i + 1] - ts[i]
            w0, w1 = 2 * h1 + h0, h1 + 2 * h0
            m[i] = (w0 + w1) / (w0 / d[i - 1] + w1 / d[i])
    return m


def campath(cut, keys):
    """连续运镜：keys = [(秒, x, y, z, yaw, pitch), ...]。起点硬切过去，之后每刻都传送一次。
    路径是过所有关键点的平滑曲线（用户 2026-11-23：原来折线 + 每 5 刻一段，看着一顿一顿的），两端带一点缓入缓出。"""
    t0, t1 = int(round(keys[0][0] * 20)), int(round(keys[-1][0] * 20))
    ts = [k[0] * 20 for k in keys]
    ch = [[k[i] for k in keys] for i in range(1, 6)]
    for i in range(1, len(keys)):                       # 朝向走最短的那一边
        ch[3][i] = ch[3][i] + 360 * round((ch[3][i - 1] - ch[3][i]) / 360.0)
    ms = [_mono_tangents(ts, v) if len(ts) > 1 else [0.0] for v in ch]

    def at(tick):
        if t1 <= t0:
            return [v[0] for v in ch]
        tick = min(max(tick, t0), t1)
        f = (tick - t0) / float(t1 - t0)
        e = f * f * (3 - 2 * f) * 0.35 + f * 0.65          # 轻度缓入缓出
        T = t0 + e * (t1 - t0)
        i = 0
        while i < len(ts) - 2 and T > ts[i + 1]:
            i += 1
        h = ts[i + 1] - ts[i]
        u = min(max((T - ts[i]) / h, 0.0), 1.0)
        h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
        return [h00 * v[i] + h10 * h * m[i] + h01 * v[i + 1] + h11 * h * m[i + 1] for v, m in zip(ch, ms)]

    def fmt(p):
        return " ".join([_num(v, 3) for v in p[:3]] + [_num(((p[3] + 180) % 360) - 180, 2), _num(p[4], 2)])
    p = at(t0)
    cut.at(t0 / 20.0, *cam(*[float(v) for v in fmt(p).split()]))
    if t1 <= t0:
        return
    cut.at((t0 + 1) / 20.0, CAM_DUR_RAW % CAM_LAG)
    end, prev = at(t1), at(t1 - 1)

    def ahead(tick):
        # 镜头末尾照最后的速度往前推，不在切镜前两刻急停
        if tick <= t1:
            return at(tick)
        return [e + (e - q) * (tick - t1) for e, q in zip(end, prev)]
    for tk in range(t0 + 1, t1 + 1):
        # 客户端落后目标约 CAM_LAG-1 刻，提前这么多发，画面和演员动作对得上
        cut.track[tk] = "in %s run tp @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] %s" % (DIM, fmt(ahead(tk + CAM_LAG - 1)))


def actor(who, x, y, z, yaw):
    base = ACTORS[who]
    tags = '"rpg.pr.actor","rpg.pr.a.%s","rpg.pr.w.%s","rpg.pr.new"' % (who, who)
    c = ["execute in %s run summon minecraft:vindicator %g %g %g {Tags:[%s],Rotation:[%gf,0f],NoAI:1b,Silent:1b,"
         "Invulnerable:1b,NoGravity:1b,PersistenceRequired:1b,attributes:[{id:\"minecraft:scale\",base:0.0625}],"
         "active_effects:[{id:\"invisibility\",duration:-1,amplifier:0,show_particles:0b}]}"
         % (DIM, x, y, z, tags, yaw)]
    c.append("execute as @e[type=minecraft:vindicator,tag=rpg.pr.new] at @s run function %s/dress" % base)
    c.append("tag @e[type=minecraft:vindicator,tag=rpg.pr.new] remove rpg.pr.new")
    return c


def anim(who, clip):
    base = ACTORS[who]
    return ["execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.%s] run function %s/anim/enter/%s"
            % (who, base, CLIP.get((who, clip), clip))]


def look(who, name):
    return ["execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.%s] run function %s/look/%s" % (who, ACTORS[who], name)]


def place(who, x, y, z, yaw):
    return ["execute in %s run tp @e[type=minecraft:vindicator,tag=rpg.pr.a.%s] %g %g %g %g 0" % (DIM, who, x, y, z, yaw)]


def drop_actor(who):
    return ["execute as @e[type=minecraft:vindicator,tag=rpg.pr.a.%s] run function rpg:prologue/cut/kill_actor" % who]


def lords(cut, sec, clip, gap=0.25, who=("beelzebub", "belial", "mammon")):
    """三位领主错开 gap 秒依次做同一个动作（齐刷刷同一帧太假）。"""
    for i, w in enumerate(who):
        cut.at(sec + i * gap, *anim(w, clip))


def face(frm, to, off=0):
    """从 frm 看向 to 的水平朝向（度），再偏 off 度（站得随意一点，不是人人正对）。"""
    import math
    return round(math.degrees(math.atan2(-(to[0] - frm[0]), to[2] - frm[2])) + off, 1)


def facecam(pos, toward, dist=3.2, ang=30, dur=0, h=1.65):
    """正面近景：机位在 pos 朝 toward 方向、偏 ang 度、离 dist 格处，看向 pos 的头部。"""
    import math
    a = math.atan2(toward[2] - pos[2], toward[0] - pos[0]) + math.radians(ang)
    x, z = pos[0] + dist * math.cos(a), pos[2] + dist * math.sin(a)
    return camlook(x, pos[1] + h + 0.1, z, pos[0], pos[1] + h - 0.1, pos[2], dur)


def knock(cut, sec, who, frm, back, yaw=YAW_E, src=None):
    """被冲击掀退：后翻滚（roll_b）同时平移 back 格（12 刻）；有 src 就背离 src 退，否则往 -x 退。返回落脚点。"""
    import math
    if src:
        dx, dz = frm[0] - src[0], frm[2] - src[2]
        n = math.hypot(dx, dz) or 1.0
        to = (round(frm[0] + back * dx / n, 2), frm[1], round(frm[2] + back * dz / n, 2))
    else:
        to = (frm[0] - back, frm[1], frm[2])
    cut.at(sec, *anim(who, "roll_b"))
    glide(cut, who, sec, frm, to, 12, yaw)
    return to


def sub(lid):
    return ["function rpg:prologue/sub/%s" % lid.lower()]


def glide(cut, who, sec, frm, to, ticks, yaw):
    """演员（怪物载体）在 ticks 刻里从 frm 平移到 to：每刻传送一次（客户端会插值，看起来是连续的）。"""
    for i in range(ticks + 1):
        f = i / float(ticks)
        p = [frm[k] + (to[k] - frm[k]) * f for k in range(3)]
        cut.at(sec + i / 20.0, *place(who, p[0], p[1], p[2], yaw))


def title(zh, en, fade_in=10, stay=70, fade_out=20, colour="#E8D9B0"):
    import json
    return ["title @a[tag=rpg.pr] times %d %d %d" % (fade_in, stay, fade_out),
            "title @a[tag=rpg.pr] subtitle %s" % json.dumps({"text": en, "color": "#BFB8A8", "italic": True}, ensure_ascii=False),
            "title @a[tag=rpg.pr] title %s" % json.dumps({"text": zh, "color": colour, "bold": True}, ensure_ascii=False)]


def P(*a):
    return ["particle %s" % " ".join(str(x) for x in a)]


def snd(name, vol=1.0, pitch=1.0):
    return ["execute as @a[tag=rpg.pr] at @s run playsound %s master @s ~ ~ ~ %g %g" % (name, vol, pitch)]


def scenes(lines):
    S = {}

    # ---------------------------------------------------------------- 场 1 开场旁白（约 35 秒，含 4 秒字卡）
    c = Cut("s1")
    c.at(0, *title(lines["U09"]["zh"], lines["U09"]["en"], 10, 60, 20), *sub("U10"))
    # 镜头一路连续移动（用户 2026-11-22：原来是滑 3 秒后干停 2～3 秒、再突然切走）
    campath(c, [(0, 0, 141, 18, YAW_N, 70), (4, 0, 133, 22, YAW_N, 60), (7, 0, 123, 27, YAW_N, 46), (9.95, 0, 115, 31, YAW_N, 34)])
    c.at(0, *actor("lucifer", -30, 81, 0, YAW_E))
    c.at(0.5, *snd("minecraft:ambient.basalt_deltas.mood", 0.8, 0.6))
    c.at(4, *sub("N01"))
    c.at(10, *sub("N02"))
    campath(c, [(10, 30, 84, -16, YAW_S, 8), (17.95, 30, 84.6, 28, YAW_S, 6)])
    c.at(18, *sub("N03"))
    campath(c, [(18, 44, 92, 6, 98, -12), (22.95, 39, 97, 4, 95, -22)])
    c.at(18, *["execute in %s positioned 0 81 0 run particle minecraft:end_rod ~ ~60 ~ 0.3 30 0.3 0.02 120 force" % DIM])
    c.at(23, *sub("N04"))
    campath(c, [(23, -37, 84.2, 0, YAW_E, 5), (28.95, -33.6, 83.4, 0, YAW_E, -10)])
    c.at(24, *anim("lucifer", "look_up"))
    c.at(29, *sub("N05"))
    campath(c, [(29, -20, 100, -30, -30, 30), (35, -8, 95, -37, -18, 27)])
    c.at(29.5, *snd("minecraft:entity.lightning_bolt.thunder", 0.6, 0.6))
    c.at(35, *drop_actor("lucifer"))
    S["s1"] = c

    # ---------------------------------------------------------------- 场 3 战场中央对话（约 22 秒）
    c = Cut("s3", auto_cam=True)
    # 三位领主散开站，远近、朝向各不相同（用户 2026-11-22「站位分散一些，站得随意一点」）
    LU3 = (-3, 81, 0)
    POS3 = {"beelzebub": ((-9.6, 81, -7.4), (-5.6, 81, -5.2), 14),     # (从哪走来, 站定处, 朝向偏角)
            "belial": ((-13.0, 81, 2.8), (-9.0, 81, 1.4), -18),
            "mammon": ((-8.8, 81, 8.0), (-4.6, 81, 5.6), 24)}
    YW3 = {k: face(v[1], LU3, v[2]) for k, v in POS3.items()}
    c.at(0, *actor("lucifer", LU3[0], LU3[1], LU3[2], YAW_E),
         *[x for k, v in POS3.items() for x in actor(k, v[0][0], v[0][1], v[0][2], face(v[0], v[1]))])
    c.at(0, *cam(-20, 85, 0.5, YAW_E, 6))
    # 各自走上前（载体在动时自动播 walk，停下回 idle），到位后转向路西法
    for (k, v), t0, n in zip(POS3.items(), (0.0, 0.3, 0.5), (62, 66, 64)):
        glide(c, k, t0, v[0], v[1], n, face(v[0], v[1]))
        c.at(t0 + n / 20.0 + 0.1, *place(k, v[1][0], v[1][1], v[1][2], YW3[k]))
    # 到位后向路西法行礼（bow 1.8 秒），之后各有各的样子
    c.at(3.35, *anim("beelzebub", "bow"))
    c.at(3.85, *anim("belial", "bow"))
    c.at(3.95, *anim("mammon", "bow"))
    c.at(5.3, *anim("beelzebub", "fold"))
    c.at(1, *cam(0.5, 82.6, 2.6, 125, 5))
    c.at(1, *anim("lucifer", "address"), *sub("D01"))
    BZ3, BL3, MM3 = POS3["beelzebub"][1], POS3["belial"][1], POS3["mammon"][1]
    c.at(6.2, *facecam(BZ3, LU3, 3.2, 35), *anim("beelzebub", "talk"), *sub("D02"))
    c.at(6.2, *P("minecraft:spore_blossom_air", BZ3[0], 82.5, BZ3[2], 0.6, 0.6, 0.6, 0, 6))
    c.at(8.4, *cam(-0.6, 82.7, 0.6, 115, 0), *sub("D03"), *anim("beelzebub", "fold"))
    c.at(9.0, *anim("belial", "showoff"))
    c.at(9.6, *anim("mammon", "showoff"))
    c.at(10.8, *facecam(BL3, LU3, 3.4, -30), *anim("belial", "talk"), *sub("D04"))
    c.at(13.8, *cam(-0.8, 82.6, 0.4, 110, 0), *sub("D05"), *anim("belial", "idle"))
    c.at(15.2, *facecam(MM3, LU3, 3.2, -35), *anim("mammon", "talk"), *sub("D06"))
    c.at(15.2, *P("minecraft:wax_on", MM3[0], 82.6, MM3[2], 0.4, 0.4, 0.4, 0, 8))
    # 收尾：路西法「我不跪」，三位领主表态站到他这边：别西卜抱臂，贝利尔、玛门举拳；镜头慢慢拉高拉远
    c.at(18.8, *camlook(2.5, 83.0, 3.0, -5.8, 81.8, 0.2), *anim("lucifer", "idle"))
    c.at(19.0, *anim("beelzebub", "fold"))
    c.at(19.3, *anim("belial", "hero"))
    c.at(19.6, *anim("mammon", "hero"))
    c.at(18.9, *camlook(4.4, 84.4, 4.4, -5.8, 81.8, 0.2, 59))
    c.at(22, "function rpg:prologue/cut/next")
    S["s3"] = c

    # ---------------------------------------------------------------- 场 4 米迦勒降临（约 11 秒，紧接场 3）
    c = Cut("s4", auto_cam=True)
    c.at(0, "function rpg:prologue/music/michael", *camlook(-3.5, 82.8, 5.5, 4, 96, 0))
    c.at(0, *["execute in %s run particle minecraft:end_rod 4 101 0 0.2 20 0.2 0.02 200 force" % DIM],
         *snd("minecraft:block.beacon.activate", 1, 0.6))
    c.at(1.5, *actor("michael", 4, 121, 0, YAW_W), *cam(-2, 82.2, -3.5, -60, -62))
    lords(c, 1.7, "look_up", 0.15)
    lords(c, 3.2, "shield", 0.08)
    c.at(1.6, *anim("michael", "dive_cry"), *vfx(L().wingburst(size=7.0), 4, 120.5, 0))
    glide(c, "michael", 1.5, (4, 121, 0), (4, 81, 0), 40, YAW_W)
    c.at(2.0, *sub("M01"))
    c.at(3.5, *cam(-5, 82.6, 3.4, -110, 0), *anim("michael", "land"), *anim("lucifer", "look_up"),
         *["execute in %s run particle minecraft:explosion_emitter 4 81.5 0 0 0 0 0 1 force" % DIM],
         *["execute in %s run particle minecraft:end_rod 4 81.5 0 2.5 0.3 2.5 0.25 160 force" % DIM],
         *snd("minecraft:entity.generic.explode", 0.8, 0.7), *snd("minecraft:entity.phantom.flap", 1.2, 0.5),
         *vfx(L().godray(), 4, 81, 0), *vfx(L().impact(size=6.0), 4, 82, 0), *vfx(L().mdecal("shockh_0", 6, kind="mshockh"), 4, 81.06, 0),
         *vfx(L().feathers_out(n=8), 4, 83, 0))
    MK = (4, 81, 0)
    K4 = {}
    for (k, v), t, back in zip(POS3.items(), (3.6, 3.65, 3.7), (1.6, 1.4, 1.8)):
        K4[k] = knock(c, t, k, v[1], back, YW3[k], src=MK)
    c.at(4.6, *anim("belial", "hero"))      # 稳住身形，摆出迎战的架势
    c.at(4.9, *anim("beelzebub", "fold"))
    # 反应镜头：被掀退的三人
    c.at(3.95, *camlook(-1.0, 83.2, 8.6, -7.0, 81.9, 0.2), *camlook(-1.4, 83.4, 9.4, -7.0, 81.9, 0.2, 26))
    c.at(5.3, *cam(-4.6, 82.8, 3.2, -112, 2))
    c.at(7, *title(lines["U11"]["zh"], lines["U11"]["en"], 5, 70, 15, "#FFD85A"), *sub("U12"))
    c.at(7, *cam(-3.8, 82.8, 3.0, -114, 2, 59))
    c.at(11, *drop_actor("michael"), *drop_actor("lucifer"), *drop_actor("beelzebub"), *drop_actor("belial"),
         *drop_actor("mammon"))
    c.at(11, "function rpg:prologue/cut/next")
    S["s4"] = c

    # ---------------------------------------------------------------- 场 6 敌基督的本源（约 25 秒）
    # 路西法被敌基督攫住、悬在半空；米迦勒也在天上，掷出脊骨。命中之后路西法才坠地
    LU, MI = (0, 90, 0), (8, 94, 0)
    c = Cut("s6", auto_cam=True)
    POS6 = {"beelzebub": ((-3.6, 81, -5.2), 18), "belial": ((-7.2, 81, 1.0), -14), "mammon": ((-2.8, 81, 4.8), -26)}
    YW6 = {k: face(v[0], (0, 81, 0), v[1]) for k, v in POS6.items()}
    c.at(0, *actor("lucifer", LU[0], LU[1], LU[2], YAW_E),
         *[x for k, v in POS6.items() for x in actor(k, v[0][0], v[0][1], v[0][2], YW6[k])],
         *actor("michael", MI[0], MI[1], MI[2], YAW_W))
    c.at(0, *camlook(-7, 84, 5, 0, 90.8, 0), *snd("minecraft:block.beacon.deactivate", 1, 0.5))
    c.at(0.5, *anim("lucifer", "seized"), "scoreboard players set #aura rpg_pr 1",
         *P("minecraft:sculk_soul", 0, 91, 0, 0.8, 1, 0.8, 0.02, 30))
    c.at(0.6, *camlook(-5, 86, 3.5, 0, 90.8, 0, 50))
    lords(c, 0.8, "look_up", 0.2)
    for t, name in ((1.5, "possessed"), (1.65, "normal"), (2.0, "possessed"), (2.2, "normal")):
        c.at(t, *look("lucifer", name), *P("minecraft:dust{color:[0.1,0.0,0.0],scale:2.0}", 0, 91, 0, 0.5, 0.8, 0.5, 0, 25))
    c.at(3.0, *camlook(2, 90, 6, 8, 95.2, 0), *anim("michael", "throw"), *vfx(L().wingburst(size=6.0), 8, 95.6, 0),
         *vfx(L().godray(hot=True), 8, 90, 0))
    c.at(4.0, "function rpg:prologue/cut/spine_throw", *snd("minecraft:item.trident.throw", 1.2, 0.6))
    c.at(4.6, *camlook(-2.6, 91.4, 3.4, 0.3, 91.2, 0), *anim("lucifer", "pierced"),
         *vfx(L().impact(hot=True, size=5.0), 0, 91.3, 0), *vfx(L().feathers_out(n=8), 0, 91.3, 0),
         *["execute in %s run particle minecraft:flash{color:[1.0,0.85,0.5,1.0]} 0 91.2 0 0 0 0 0 1 force" % DIM],
         *P("minecraft:flame", 0, 91.2, 0, 0.4, 0.4, 0.4, 0.08, 40),
         *snd("minecraft:item.trident.hit", 1.2, 0.6), *snd("minecraft:entity.generic.hurt", 1, 0.5))
    c.at(5.1, *camlook(-9, 84, 7, 0, 85, 0))
    glide(c, "lucifer", 5.2, LU, (0, 81, 0), 14, YAW_E)
    c.at(5.95, *vfx(L().impact(hot=True, size=6.0), 0, 81.6, 0), *vfx(L().mdecal("shock_0", 7, kind="mshock"), 0, 81.06, 0),
         *vfx(L().smoke_puff(size=4.0), 1.5, 81.5, 1), *vfx(L().smoke_puff(size=4.0), -1.5, 81.5, -1),
         *P("minecraft:block{block_state:\"minecraft:polished_blackstone_bricks\"}", 0, 81.2, 0, 1.5, 0.3, 1.5, 0.2, 120),
         *snd("minecraft:entity.generic.explode", 1.2, 0.5), *snd("minecraft:entity.iron_golem.damage", 1.2, 0.5))
    BZ = knock(c, 5.95, "beelzebub", POS6["beelzebub"][0], 1.5, YW6["beelzebub"], src=(0, 81, 0))
    BL = knock(c, 6.0, "belial", POS6["belial"][0], 1.2, YW6["belial"], src=(0, 81, 0))
    MM = knock(c, 6.05, "mammon", POS6["mammon"][0], 1.8, YW6["mammon"], src=(0, 81, 0))
    # 裂缝张开：抬臂挡住那股冲击；别西卜僵立着盯住裂缝（他第一个走），贝利尔、玛门跪伏，轮到谁谁起身化烟
    lords(c, 7.0, "shield", 0.12)
    c.at(8.0, *anim("beelzebub", "stun"))
    for who, t, up in (("belial", 8.0, 11.7), ("mammon", 8.3, 14.9)):
        c.at(t, *anim(who, "kneel_down"))
        c.at(t + 1.25, *anim(who, "kneel_idle"))
        c.at(up, *anim(who, "kneel_up"))
    c.at(7.0, *anim("lucifer", "tear"), *look("lucifer", "possessed"), "scoreboard players set #rift rpg_pr 1",
         *vfx(L().impact(size=8.0), *RIFT), *P("minecraft:reverse_portal", RIFT[0], RIFT[1], RIFT[2], 3, 4, 0.3, 0.6, 400),
         *snd("minecraft:block.end_portal.spawn", 0.9, 0.6), *snd("minecraft:entity.wither.spawn", 0.5, 1.6))
    c.at(7.0, *camlook(5, 82.5, 6, 0, 85, -8), *camlook(6.5, 83, 8.5, 0, 85.5, -8, 40))
    c.at(9.5, *camlook(-6, 84.5, 13, -4.5, 83.2, -1), *sub("E01"))
    wisp(c, "beelzebub", 10.0, BZ, "[0.7,0.8,0.2]", "minecraft:spore_blossom_air")
    c.at(12.8, *sub("E02"))
    wisp(c, "belial", 13.0, BL, "[0.55,0.2,0.75]", "minecraft:witch")
    c.at(16.0, *sub("E03"))
    wisp(c, "mammon", 16.2, MM, "[1.0,0.8,0.2]", "minecraft:wax_on")
    c.at(18.8, *camlook(3, 82.2, 3, 0, 82.6, -6), *anim("lucifer", "reach"))
    c.at(20.3, *camlook(-5.5, 82, 5, 4, 87, 0), *anim("michael", "stomp"), *vfx(L().wingburst(size=7.0), MI[0], MI[1] + 1.6, MI[2]),
         *snd("minecraft:entity.phantom.swoop", 1.4, 0.6))
    glide(c, "michael", 20.3, MI, (1.5, 81, 0), 18, YAW_W)
    c.at(21.25, "function rpg:prologue/cut/shatter", *anim("lucifer", "stomped"),
         *vfx(L().godray(hot=True), 1.5, 81, 0), *vfx(L().impact(hot=True, size=8.0), 1.5, 82, 0),
         *vfx(L().mdecal("shock_0", 9, kind="mshock"), 0, 80.1, 0),
         *snd("minecraft:entity.generic.explode", 1.4, 0.6), *snd("minecraft:entity.warden.sonic_boom", 0.8, 0.7))
    glide(c, "lucifer", 21.4, (0, 81, 0), (0, FLOOR, 0), 40, YAW_E)
    c.at(23.5, *cam(0.3, 96, 0.3, YAW_E, 90))
    c.at(23.4, *P("minecraft:large_smoke", 0, 60, 0, 3, 8, 3, 0.02, 200))
    c.at(23.45, *vfx(L().impact(hot=True, size=6.0), 0, FLOOR + 0.6, 0), *snd("minecraft:entity.generic.explode", 0.8, 0.4))
    c.at(25, "function rpg:prologue/cut/next")
    S["s6"] = c

    # ---------------------------------------------------------------- 场 7 分离（约 33 秒）
    # 路西法躺在石台下的大洞穴底；绿烟（敌基督）从他身上升起，穿过洞口钻进裂缝；米迦勒悬在洞口上方俯视，之后升天离去
    MH = (0, 84, -2)
    c = Cut("s7", auto_cam=True)
    c.at(0, "scoreboard players set #smoke rpg_pr 1", *sub("N06"), *cam(0.3, 95.6, 0.3, YAW_E, 90))
    c.at(0.5, *cam(0.3, 92, 0.3, YAW_E, 90, 59))
    c.at(3.0, *camlook(5, 88, 5, 0, 84, -6, 59))
    c.at(6.0, "scoreboard players set #rift rpg_pr 2", "scoreboard players set #smoke rpg_pr 0",
         *["execute in %s run particle minecraft:flash{color:[0.5,0.3,0.8,1.0]} %g %g %g 0 0 0 0 1 force" % ((DIM,) + RIFT)],
         *vfx(L().impact(size=8.0), *RIFT), *snd("minecraft:block.end_portal_frame.fill", 1, 0.5))
    c.at(7.5, "scoreboard players set #rift rpg_pr 0")
    c.at(8.0, *sub("N07"), *cam(0.3, 62, 0.3, YAW_E, 90, 59), "scoreboard players set #aura rpg_pr 2")
    c.at(11.0, *camlook(6, 41, 6, 0, FLOOR + 0.5, 0, 50))
    c.at(13.5, *anim("lucifer", "pit_rise"), *sub("X01"), *snd("minecraft:entity.warden.heartbeat", 1.2, 0.6))
    c.at(15.5, *camlook(0.8, FLOOR + 2.4, 1.4, MH[0], MH[1] + 1.5, MH[2]), *drop_actor("michael"),
         *actor("michael", MH[0], MH[1], MH[2], YAW_S), *anim("michael", "look_down"), *sub("X02"),
         *vfx(L().godray(), MH[0], 81, MH[2]))
    c.at(18.0, *cam(0.3, 92, 0.3, YAW_E, 90), *sub("N08"), "scoreboard players set #aura rpg_pr 0",
         *P("minecraft:large_smoke", 0, FLOOR + 4, 0, 2, 3, 2, 0.02, 120))
    glide(c, "lucifer", 18.2, (0, FLOOR, 0), (0, FLOOR - 4, 0), 50, YAW_E)
    c.at(21.5, *sub("N09"), *camlook(0, 82, 8, MH[0], MH[1] + 4, MH[2]), *anim("michael", "rise"),
         *snd("minecraft:block.beacon.power_select", 1, 1.2), *vfx(L().godray(), MH[0], 81, MH[2]))
    glide(c, "michael", 21.6, MH, (MH[0], 98, MH[2]), 60, YAW_S)
    c.at(24.5, *vfx(L().wingburst(size=9.0), MH[0], 99.6, MH[2]), *vfx(L().impact(size=7.0), MH[0], 99.6, MH[2]),
         *vfx(L().feathers_out(n=8), MH[0], 99.6, MH[2]),
         *["execute in %s run particle minecraft:flash{color:[1.0,0.9,0.6,1.0]} 0 99.6 -2 0 0 0 0 1 force" % DIM])
    c.at(25.0, *drop_actor("michael"), *P("minecraft:end_rod", 0, 99.6, -2, 0.8, 1.5, 0.8, 0.15, 160),
         *snd("minecraft:block.amethyst_block.resonate", 1, 1.4))
    c.at(26.5, *drop_actor("lucifer"), "function rpg:prologue/cut/feather")
    c.at(27.5, *cam(0, 88, 2.5, YAW_N, 30, 50))
    c.at(30, *title(lines["U13"]["zh"], lines["U13"]["en"], 10, 60, 20))
    c.at(33, "function rpg:prologue/cut/next")
    S["s7"] = c
    return S


def write(fn, lines):
    S = scenes(lines)
    for c in S.values():
        c.smooth_cams()
    order = ["s1", "s3", "s4", "s6", "s7"]
    for name, c in S.items():
        disp = []
        for t in sorted(c.beats):
            fn("cut/%s/b%d" % (name, t), c.beats[t])
            disp.append("execute if score #ct rpg_pr matches %d run function rpg:prologue/cut/%s/b%d" % (t, name, t))
        # 机位轨道：每刻一条传送，按 20 刻一组分派（放在 beat 之后：硬切后一刻先改插值再传送）
        groups = {}
        for t in sorted(c.track):
            groups.setdefault(t // 20, []).append(
                "execute if score #ct rpg_pr matches %d %s" % (t, c.track[t]))
        for g in sorted(groups):
            fn("cut/%s/cam/c%d" % (name, g), groups[g])
            disp.append("execute if score #ct rpg_pr matches %d..%d run function rpg:prologue/cut/%s/cam/c%d"
                        % (g * 20, g * 20 + 19, name, g))
        if name == "s1":
            disp.append("execute if score #ct rpg_pr matches %d.. run function rpg:prologue/cut/next" % (c.end_tick() + 1))
        disp.append("scoreboard players add #ct rpg_pr 1")      # 先分派再加一：第 0 刻的镜头与演员也要放
        fn("cut/%s/tick" % name, disp)
    # 进出过场：玩家切旁观、附身机位；退出时由流程放回原位（prologue/flow）
    fn("cut/begin", [
        "scoreboard players set #ct rpg_pr 0",
        "kill @e[type=minecraft:item_display,tag=rpg.pr.cam]",
        "execute in %s run summon minecraft:item_display 0 120 0 {Tags:[\"rpg.pr.cam\",\"rpg.pr.ent\"],teleport_duration:0}" % DIM,
        "gamemode spectator @a[tag=rpg.pr]",
        "execute as @a[tag=rpg.pr] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] @s",
    ])
    fn("cut/tick", [
        "# 过场中每刻：按段分派；每 10 刻把镜头重新附一次（旁观者按潜行会脱离附身）",
        "execute if score #cut rpg_pr matches 1 run function rpg:prologue/cut/s1/tick",
        "execute if score #cut rpg_pr matches 3 run function rpg:prologue/cut/s3/tick",
        "execute if score #cut rpg_pr matches 4 run function rpg:prologue/cut/s4/tick",
        "execute if score #cut rpg_pr matches 6 run function rpg:prologue/cut/s6/tick",
        "execute if score #cut rpg_pr matches 7 run function rpg:prologue/cut/s7/tick",
        "scoreboard players operation #m rpg_pr = #ct rpg_pr",
        "scoreboard players operation #m rpg_pr %= #ten rpg_pr",
        "execute if score #m rpg_pr matches 0 as @a[tag=rpg.pr,gamemode=spectator] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] @s",
        "function rpg:prologue/cut/fx_tick",
    ])
    fn("cut/fx_tick", [
        "# 过场里持续的特效：裂缝（#rift 1 张开中 / 2 合上中）、路西法身上的暗红黑气（#aura）、飘向裂缝的绿烟（#smoke）",
        "execute if score #rift rpg_pr matches 1 in %s run particle minecraft:reverse_portal %g %g %g 2.6 3.6 0.3 0.05 30 force" % ((DIM,) + RIFT),
        "execute if score #rift rpg_pr matches 1 in %s run particle minecraft:dust{color:[0.48,0.25,0.75],scale:2.4} %g %g %g 2.4 3.4 0.2 0 10 force" % ((DIM,) + RIFT),
        "execute if score #rift rpg_pr matches 1 in %s run particle minecraft:portal %g %g %g 3 4 0.5 0.6 12 force" % ((DIM,) + RIFT),
        "execute if score #rift rpg_pr matches 2 in %s run particle minecraft:reverse_portal %g %g %g 1.2 2 0.2 0.02 10 force" % ((DIM,) + RIFT),
        "# 地下城特效（rpg:michael_vfx）：米迦勒 Boss 不在场时由这里推进",
        "execute unless entity @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1] as @e[tag=rpg.mkb.fx] at @s run function rpg:michael_boss/fx/tick",
        "execute if score #aura rpg_pr matches 1.. as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer] at @s run particle minecraft:dust{color:[0.45,0.05,0.05],scale:1.6} ~ ~1 ~ 0.4 0.8 0.4 0 4 force",
        "execute if score #aura rpg_pr matches 1.. as @e[type=minecraft:vindicator,tag=rpg.pr.a.lucifer] at @s run particle minecraft:large_smoke ~ ~0.6 ~ 0.3 0.3 0.3 0.01 1 force",
        "execute if score #smoke rpg_pr matches 1 as @e[type=minecraft:marker,tag=rpg.pr.smoke] at @s run function rpg:prologue/cut/smoke_step",
        "execute unless score #smoke rpg_pr matches 1 run kill @e[type=minecraft:item_display,tag=rpg.pr.smokev]",
        "# 序列帧（Codex 画的裂缝 rift_0..7、绿烟 smoke_0..7，每 3 刻一帧）",
        "scoreboard players add #fxc rpg_pr 1",
        "execute if score #fxc rpg_pr matches 3.. run function rpg:prologue/cut/fx_frame",
        "execute if score #rift rpg_pr matches 1.. unless entity @e[type=minecraft:item_display,tag=rpg.pr.riftv] in %s run summon "
        "minecraft:item_display %g %g %g {Tags:[\"rpg.pr.riftv\",\"rpg.pr.ent\"],billboard:\"vertical\",brightness:{sky:15,block:15},"
        "item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:prologue_fx/rift_0\"}},item_display:\"fixed\","
        "transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[14f,17f,14f]}}" % ((DIM,) + RIFT),
        "execute if score #rift rpg_pr matches 0 run kill @e[type=minecraft:item_display,tag=rpg.pr.riftv]",
    ])
    fn("cut/fx_frame", [
        "scoreboard players set #fxc rpg_pr 0",
        "# 裂缝：张开时 0→7，之后在 4～7 之间循环；合上时倒放，放完就撤",
        "execute if score #rift rpg_pr matches 1 run scoreboard players add #rf rpg_pr 1",
        "execute if score #rift rpg_pr matches 1 if score #rf rpg_pr matches 8.. run scoreboard players set #rf rpg_pr 4",
        "execute if score #rift rpg_pr matches 2 run scoreboard players remove #rf rpg_pr 1",
        "execute if score #rift rpg_pr matches 0 run scoreboard players set #rf rpg_pr -1",
        "execute if score #rf rpg_pr matches ..-1 run kill @e[type=minecraft:item_display,tag=rpg.pr.riftv]",
        "execute if score #rf rpg_pr matches ..-1 if score #rift rpg_pr matches 2 run scoreboard players set #rift rpg_pr 0",
        "execute if score #rf rpg_pr matches ..-1 run scoreboard players set #rf rpg_pr 0",
    ] + ["execute if score #rf rpg_pr matches %d as @e[type=minecraft:item_display,tag=rpg.pr.riftv] run data modify entity @s "
         "item.components.\"minecraft:item_model\" set value \"rpg:prologue_fx/rift_%d\"" % (i, i) for i in range(8)] + [
        "scoreboard players add #sf rpg_pr 1",
        "execute if score #sf rpg_pr matches 8.. run scoreboard players set #sf rpg_pr 0",
    ] + ["execute if score #sf rpg_pr matches %d as @e[type=minecraft:item_display,tag=rpg.pr.smokev] run data modify entity @s "
         "item.components.\"minecraft:item_model\" set value \"rpg:prologue_fx/smoke_%d\"" % (i, i) for i in range(8)]
      + ["execute if score #sf rpg_pr matches %d as @e[type=minecraft:item_display,tag=rpg.pr.wisp] run data modify entity @s "
         "item.components.\"minecraft:item_model\" set value \"rpg:prologue_fx/smoke_%d\"" % (i, i) for i in range(8)])
    fn("cut/smoke_step", [
        "# 一缕绿烟：从洞底的路西法身上升起，穿过洞口往上飘，最后钻进裂缝",
        "particle minecraft:dust{color:[0.37,0.84,0.55],scale:1.8} ~ ~ ~ 0.15 0.15 0.15 0 6 force",
        "particle minecraft:dust{color:[0.85,1.0,0.9],scale:0.9} ~ ~ ~ 0.05 0.05 0.05 0 2 force",
        "particle minecraft:campfire_cosy_smoke ~ ~ ~ 0.05 0.05 0.05 0.005 1 force",
        "execute unless entity @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=..2] run summon minecraft:item_display ~ ~ ~ "
        "{Tags:[\"rpg.pr.smokev\",\"rpg.pr.ent\"],billboard:\"center\",teleport_duration:1,brightness:{sky:15,block:15},"
        "item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:prologue_fx/smoke_0\"}},item_display:\"fixed\","
        "transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.6f,1.6f,1.6f]}}",
        "tp @e[type=minecraft:item_display,tag=rpg.pr.smokev,distance=..2,limit=1,sort=nearest] ~ ~ ~",
        "execute if entity @s[y=80,dy=12] facing %g %g %g run tp @s ^ ^ ^0.45" % RIFT,
        "execute unless entity @s[y=80,dy=12] run tp @s ~0.01 ~0.65 ~-0.02",
    ])
    fn("cut/kill_actor", ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])
    fn("cut/spine_throw", [
        "# 米迦勒脊骨：一件脊骨的 item_display 从他手里平滑飞到路西法胸口（12 刻）",
        "execute in %s run summon minecraft:item_display 7.2 95.4 0 {Tags:[\"rpg.pr.spine\",\"rpg.pr.ent\"],"
        "item:{id:\"minecraft:netherite_spear\",count:1,components:{\"minecraft:custom_model_data\":{floats:[1110040f]}}},"
        "item_display:\"none\",teleport_duration:12,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],"
        "translation:[0f,0f,0f],scale:[2f,2f,2f]},Rotation:[90f,31f]}" % DIM,
        "schedule function rpg:prologue/cut/spine_go 1t",
    ])
    fn("cut/spine_go", ["execute in %s run tp @e[type=minecraft:item_display,tag=rpg.pr.spine] 0.4 91.3 0" % DIM])
    fn("cut/shatter", [
        "# 米迦勒一脚踩碎石台：石台方块拆掉，碎块往下掉",
        "execute in %s run fill -4 80 -4 4 80 4 minecraft:air replace #rpg:prologue_platform" % DIM,
        "execute in %s run particle minecraft:block{block_state:\"minecraft:polished_blackstone_bricks\"} 0 80.5 0 2.5 0.4 2.5 0.2 300 force" % DIM,
        "execute in %s run particle minecraft:explosion 0 80.5 0 2 0.3 2 0 6 force" % DIM,
        "kill @e[type=minecraft:item_display,tag=rpg.pr.spine]",
        "execute in %s run summon minecraft:marker 0 %g 0 {Tags:[\"rpg.pr.smoke\",\"rpg.pr.ent\"]}" % (DIM, FLOOR + 1.5),
    ])
    fn("cut/feather", [
        "# 最后一片羽毛：米迦勒 Boss 现成的羽毛模型，转着飘下来",
        "execute in %s run summon minecraft:item_display 0 99 -2 {Tags:[\"rpg.pr.feather\",\"rpg.pr.ent\"],"
        "item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rpg:prologue_feather\"}},"
        "item_display:\"fixed\",teleport_duration:59,Rotation:[0f,0f]}" % DIM,
        "schedule function rpg:prologue/cut/feather_fall 2t",
    ])
    fn("cut/feather_fall", ["execute in %s run tp @e[type=minecraft:item_display,tag=rpg.pr.feather] 0 86.5 -1 200 0" % DIM])
    return S
