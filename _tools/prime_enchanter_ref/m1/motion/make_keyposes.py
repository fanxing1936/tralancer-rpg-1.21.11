"""Build the reviewed key-pose table from the original GIF timing."""
from __future__ import annotations

import json
from pathlib import Path

from extract_gifs import MOTION, ORIGINALS, make_board, read_frames


# Frames were selected by comparing the full canvases and locally cropped details.
# A cue denotes a visible pose landmark, not a decoded gameplay event.
POSES = {
    "idle": [
        (0, "双拳抬至胸脸前，重心平稳，披风沿背下垂"),
        (4, "头与肩一同轻抬，拳位随之略升"),
        (9, "披风靠近背后，头身回落"),
        (14, "披风下段向后分开，拳架基本保持"),
        (19, "肩与前臂回到起势附近"),
        (23, "最后一帧仍维持拳架，循环接回首姿"),
    ],
    "walk": [
        (0, "侧视方向朝左，躯干略前倾，一腿前摆"),
        (4, "前腿回收，反侧臂在肩下回摆"),
        (8, "腿在身体下交会，披风向后拖曳"),
        (12, "前后腿交换并张开，反相摆臂"),
        (16, "张步缩回，膝脚向下接近中位"),
        (21, "回到与首帧相近的跨步相位"),
    ],
    "spawn": [
        (0, "空帧，模型还未进入 GIF 可见范围"),
        (6, "首帧可见，从上方低头折体下坠，披风近竖直"),
        (7, "双拳朝下进入最低伏姿候选，披风仍上翘"),
        (10, "低伏稳定，披风被甩至后方近水平"),
        (26, "低头屈膝的保持段收尾"),
        (32, "头肩与髋一起抬起，双拳先垂在身侧"),
        (38, "双拳抬回前方，接近常态拳架"),
        (42, "举拳后有一次短暂的不对称回摆"),
        (49, "另一拳补回胸前"),
        (56, "回归待机"),
    ],
    "death": [
        (0, "双臂较松，身体直立"),
        (5, "仰头挺胸，两臂向侧前弹开"),
        (22, "肩身前栽，双拳降低，跨腿站稳"),
        (34, "上身反向仰起，腿收拢，披风向后"),
        (45, "身体降低，屈腿的支撑姿势保持"),
        (68, "头胸俯至较低，双拳与披风向前后分开"),
        (80, "头肩短暂恢复，髋仍低"),
        (103, "一拳再次抬起，头仰起"),
        (110, "向前失去支撑，身体开始转为水平"),
        (112, "俯卧落定，双拳向两侧，两片披风搭在背上"),
        (136, "末帧保持倒地"),
    ],
    "forward_strike": [
        (0, "待机拳架"),
        (7, "近侧拳后撤，前腿开始屈抬"),
        (14, "身向前预载，披风折向后方"),
        (32, "末段蓄势，仍处于短时间持姿"),
        (34, "抬拳并转胸，准备爆发"),
        (36, "右拳向前最大伸展，腿打开，披风被甩起"),
        (39, "肩胯保持在冲拳端势，披风端继续滞后摆动"),
        (50, "冲拳保持结束，准备收回"),
        (55, "胸与拳回转，披风反摆"),
        (59, "归待机拳架"),
    ],
    "fury_fist": [
        (0, "起手为待机拳架"),
        (13, "拳在身前平伸，身体换重"),
        (18, "第一串中向前的拳达到伸出轮廓"),
        (27, "收拳并交叠于胸前，脚步仍开"),
        (33, "再一次转体向前出拳，披风向侧后甩开"),
        (47, "两拳靠近头胸，身体短暂低伏"),
        (53, "拳放下，短暂停顿开始"),
        (76, "重新举起拳架，准备第二串"),
        (90, "第二串首次迅速向前伸拳"),
        (95, "手臂在前方达到极端，远臂向侧展开"),
        (103, "前拳回收，反侧拳高举，身体有扭转"),
        (108, "再向前伸拳，披风和头巾带反甩"),
        (120, "收拢下蹲后蓄力，头胸低"),
        (126, "起跳达到高点，双拳在头侧，双腿向后收"),
        (130, "开始急落，披风竖向上甩"),
        (132, "双拳向下，进入地击的低伏姿势"),
        (145, "低伏保持，披风贴近背面"),
        (159, "先抬头与一拳，起身收势"),
        (165, "回到待机首姿"),
    ],
    "launch": [
        (0, "起手为待机拳架"),
        (8, "身体降低，腿收拢，前臂向脸前"),
        (23, "低伏持势即将结束"),
        (26, "从上边界离开，双腿与躯干延展"),
        (27, "从此帧开始完全透明"),
        (52, "末个完全透明帧"),
        (53, "重新可见且已经进入低伏触地姿，披风竖起"),
        (57, "冲击后披风回摆，身体保持低伏"),
        (75, "身体进一步贴低，两臂朝地"),
        (83, "抬头肩，拳逐渐离地"),
        (94, "回到待机拳架"),
    ],
    "lightning_slam": [
        (0, "起手为待机拳架"),
        (13, "腿打开，右臂侧伸，左拳保持在头侧"),
        (35, "延长蓄势姿，重量略移动"),
        (47, "迅速升空，双腿收起，拳靠近头"),
        (52, "接近跃升高点，身体直立，左拳保持头侧"),
        (56, "开始前旋，头肩与胸髋转向地面"),
        (61, "折体急落，披风和头巾带被甩直"),
        (64, "进入最低伏落点，拳朝地，披风仍竖立"),
        (68, "披风恢复为向后弯，身体仍低伏"),
        (88, "短暂再低头，作恢复前的反摆"),
        (97, "双拳离地，抬起躯干"),
        (105, "回待机"),
    ],
    "overcharge": [
        (0, "起手为待机拳架"),
        (10, "跨步降低肩身，左拳移到脸侧，右拳下探"),
        (28, "延续带有细微晃动的预载"),
        (39, "左拳抬到额侧，右臂向外压下"),
        (46, "单拳在头侧接近竖直，进入完整端势"),
        (60, "保持头侧举拳，腿仍分开"),
        (68, "持势即将结束"),
        (78, "左拳离开头侧，右拳抬回"),
        (85, "回到待机拳架"),
    ],
    "staggered": [
        (0, "双臂初始较松，身体直立"),
        (4, "躯干迅速前折，披风被甩起"),
        (11, "转为明显后仰，抬一脚，双臂拉开"),
        (22, "维持失衡姿，头胸后仰"),
        (34, "逐渐收回抬起的腿"),
        (38, "重新支撑时身体前倾，披风向后甩"),
        (45, "拳从侧面补回至脸前"),
        (54, "回归待机拳架"),
    ],
    "summon": [
        (0, "起手为待机拳架"),
        (8, "屈膝低身，双拳预载，披风向后"),
        (13, "开始仰头举拳，双臂迅速张开"),
        (14, "双拳首次完整举起，抬头挺胸"),
        (24, "双拳高举的保持段，披风小摆"),
        (33, "最后一段完整高举姿势"),
        (38, "两臂下放，开始回身"),
        (44, "拳架下沉后弹回，披风向后反摆"),
        (53, "回归待机"),
    ],
}

RUNTIME_NAMES = {"spawn": "appear", "staggered": "hurt"}
POSE_CUES = {
    "spawn": [(7, "landing", "首次低伏落地候选")],
    "death": [(112, "fall", "俯卧落定候选")],
    "forward_strike": [(36, "strike", "右拳最大前伸")],
    "fury_fist": [(18, "first_forward_reach", "第一串向前伸拳轮廓"),
                  (33, "first_turning_reach", "第一串转身伸拳轮廓"),
                  (90, "second_first_reach", "第二串首个迅速伸拳轮廓"),
                  (95, "second_wide_reach", "第二串前臂拉开轮廓"),
                  (108, "second_turning_reach", "第二串转身伸拳轮廓"),
                  (132, "slam", "双拳落地候选")],
    "launch": [(27, "off_frame_begin", "源 GIF 从此完全透明"),
               (53, "return_landing", "首个回归可见帧，低伏触地")],
    "lightning_slam": [(47, "jump", "开始明显离地"), (64, "slam", "进入低伏着地端姿")],
    "overcharge": [(46, "charge_hold", "完整举拳端势，实机电波发出时刻待确认")],
    "staggered": [(11, "recoil", "后仰失衡端势")],
    "summon": [(14, "raised_fists", "双拳首次完整举起，实机生成时刻待确认")],
}


def tick(ms):
    return (ms + 25) // 50


def write_report(out, timing):
    lines = [
        "# 首席附魔师动作素材与关键姿态",
        "",
        "十一段动作均有 Minecraft Wiki 发布的原作 GIF。每个源文件完整解码，"
        "按 GIF 编码的 40／50 ms delay 累加计算时间。总时长包含末帧停留，"
        "末帧起点单独列出。GIF 自身的无限循环用于网页展示。下表的运行循环只给 idle 和 walk。",
        "",
        "[Minecraft Wiki 角色与图库](https://minecraft.wiki/w/Dungeons_II:Prime_Enchanter)",
        "",
        "| Clip | 源动作 | 帧数 | GIF 时长 | 末帧起点 | 建议 20 TPS 时长 | 运行循环 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for key, clip in out["clips"].items():
        src = timing[key]
        name = clip["gif"].removeprefix("MCD2_Prime_Enchanter_").removesuffix(".gif")
        lines.append(
            f"| `{clip['name']}` | {name} | {len(src['frames'])} | {clip['duration_ms']/1000:.3f} s"
            f" | {src['last_frame_start_ms']/1000:.3f} s | {clip['nominal_ticks']} tick"
            f" | {'是' if clip['loop'] else '否'} |"
        )
    lines.extend([
        "",
        "建议 tick 按源时刻最近的 50 ms 四舍五入。关键姿态表区分源画面时间和项目动作锚点。"
        "GIF 仅显示角色姿态，以下出手点属于从可见端姿提议的接口约定。"
        "实机伤害、召怪、光束与地面电波的触发时间还未逐帧确认。",
        "",
        "| Clip | 可见锚点 | 源帧 | GIF 时刻 | 建议 tick |",
        "|---|---|---:|---:|---:|",
    ])
    for clip in out["clips"].values():
        for cue in clip["pose_cues"]:
            lines.append(f"| `{clip['name']}` | {cue['basis']} | {cue['frame']}"
                         f" | {cue['start_ms']/1000:.3f} s | {cue['suggested_tick']} |")
    lines.extend([
        "",
        "- Spawn 在 0–0.250 s 没有可见像素，f6 从上方进入，f7 进入低伏落地姿态。"
        "Launch 在 1.130–2.210 s 没有可见像素。两段首末姿可以从 GIF 对齐，纯旋转、位移通道只能复刻姿态和出入画移动。"
        "完整显隐需要另一个显示控制入口。",
        "- Forward Strike 在 f35–36 的前伸轮廓比常规拳臂更长。固定尺寸部件可以用肩、肘、拳的前伸与根位移保留冲击感，"
        "实际的短暂局部缩放属于改编差异。",
        "- Fury Fist GIF 有前后两串拳、中段复位和末尾跃起砸地。"
        "两串内的出拳帧可用于核对动作节奏，GIF 里的伸拳次数与项目伤害次数需分别约定。",
        "- Lightning Slam 保留跃升、空中持姿、折体下坠和落地。原 GIF 在最高点裁掉了少量画面边缘，"
        "整段画布纵向很长。全画幅对照用于核对移动，细节板按角色包围框居中后用于核对肢体角度。",
        "- Overcharge GIF 的可见端势是左拳竖举至头侧，另一拳下压，脚呈分开支撑。"
        "项目玩法若需要浮空或延长保持，属于另行设计。GIF 的 3.58 s 时长仍单独保留。",
        "- 静态拳套发光颜色取自下方实机证据。GIF 的角色运动可以匹配，粒子、电环、模糊和闪烁不在本动作表的拟合范围。",
        "",
        "## 原作过场与实机补证",
        "",
        "Video Game News 原录 1080p60。9.800–11.700 s 的头部特写可见青色额纹、灰鼻、白色眼发光。"
        "12.300–14.500 s 提供落地至举拳正面姿势，14.500 s 的角色右拳呈青、左拳呈黄。"
        "15.000 s 背面和 15.500 s 侧后镜头可核对披风条带、侧肩和下摆。"
        "17.000–20.500 s 属于过场单拳抬起及双拳交叉。22.000–24.000 s 提供俯视落地冰圈参考。",
        "",
        "[Video Game News 原录](https://www.youtube.com/watch?v=KorV2SgmFWU) · [过场对照](gameplay/intro/contact.jpg)"
        " · [帧时间和哈希](gameplay/intro/source.json)",
        "",
        "原录 28 秒附近进入 Boss HUD。32–33 s、46–50 s、66–68 s 有可辨认的黄电和青冰效果连续变化。"
        "竞技场远视画面容易被多人和粒子遮挡，动作角度优先对照 Wiki 模型 GIF。"
        "补证帧保留 HUD 和原背景，便于确认来源与场景。",
        "",
        "[竞技场对照](gameplay/arena/contact.jpg) · [帧时间和哈希](gameplay/arena/source.json)",
        "",
        "官方开场动画 00:56–01:16 和 01:18–01:20 有角色合成前后及全身镜头。"
        "官方宣传插画可交叉核对拳套发光和人物轮廓。开场动画中的道具和仪式作为造型参考。",
        "",
        "[Mojang 官方开场动画](https://www.youtube.com/watch?v=WD9GtlgU8_c&t=56s)"
        " · [官方宣传插画](https://www.minecraft.net/en-us/article/dungeons-ii-battle-for-tokyo)",
        "",
        "## 关键姿态",
        "",
    ])
    for key, clip in out["clips"].items():
        lines.extend([
            f"### {clip['name']}",
            "",
            f"[关键姿态板]({clip['keypose_sheet']}) · [整段均匀时间对照](contact_sheets/{key}.jpg)",
            "",
            "| 源帧 | GIF 起点 | 建议 tick | 观察 |",
            "|---:|---:|---:|---|",
        ])
        for pose in clip["keyposes"]:
            lines.append(f"| [{pose['frame']}]({pose['image']}) | {pose['start_ms']/1000:.3f} s"
                         f" | {pose['nearest_tick']} | {pose['pose']} |")
        lines.append("")
    lines.extend([
        "## 复现",
        "",
        "在仓库根目录运行下列命令。GIF 的所有帧都能从 `originals` 重新解码，"
        "项目目录只留选出的姿态 PNG 和对照板。加入 `--all-frames` 可以在指定目录导出全部 PNG。",
        "",
        "```powershell",
        "python _tools/prime_enchanter_ref/m1/motion/extract_gifs.py --samples 25",
        "python _tools/prime_enchanter_ref/m1/motion/make_keyposes.py",
        "```",
        "",
        "实机视频的源轨为 VP9 WebM、YouTube itag 303、1920×1080 60 FPS、仅画面。"
        "源文件 80,942,115 字节，SHA-256 为"
        " `4f9333f5765da13a9acbea62f2c27d792e823097b94e63b43338c7ff22539c2e`。"
        "现存源文件位于工作目录 `D:/agent/codex/TRA/work/prime_enchanter_sources/source_KorV2SgmFWU.webm`。",
        "",
        "```powershell",
        "uvx --from 'yt-dlp[default]' yt-dlp --no-playlist --js-runtimes node -f 303 -o 'source_KorV2SgmFWU.webm' 'https://www.youtube.com/watch?v=KorV2SgmFWU'",
        "python _tools/prime_enchanter_ref/m1/motion/extract_gameplay.py 'D:/agent/codex/TRA/work/prime_enchanter_sources/source_KorV2SgmFWU.webm' --times 4 9.8 10.3 11.7 12.3 13 13.5 14 14.5 15 15.5 16 16.5 17 18.5 19.5 20.5 21 22 24 --name intro",
        "python _tools/prime_enchanter_ref/m1/motion/extract_gameplay.py 'D:/agent/codex/TRA/work/prime_enchanter_sources/source_KorV2SgmFWU.webm' --times 32 33 38 46 48 50 66 68 --name arena",
        "```",
        "",
        "原作角色与游戏画面版权归 Mojang 等权利人所有。实机录制由 Video Game News 发布。"
        "本项目使用这些帧进行非商业模型对照，与 Mojang 无关联。",
        "",
    ])
    (MOTION / "MOTION_STUDY.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    timing = json.loads((MOTION / "gif_timing.json").read_text(encoding="utf-8"))["clips"]
    out = {"source_type": "original-game capture GIFs published by Minecraft Wiki",
           "tick_rate": 20, "tick_rule": "nearest 50 ms, half-up", "clips": {}}
    for key, poses in POSES.items():
        clip = timing[key]
        rows = clip["frames"]
        frames, _ = read_frames(ORIGINALS / clip["source_file"])
        target = MOTION / "keypose_sheets" / f"{key}.jpg"
        make_board(key, frames, rows, [idx for idx, _ in poses], target)
        for idx, _ in poses:
            path = MOTION / "frames" / key / f"{idx:04d}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.is_file():
                frames[idx].save(path)
        out["clips"][key] = {
            "name": RUNTIME_NAMES.get(key, key),
            "gif": clip["source_file"],
            "duration_ms": clip["duration_ms"],
            "nominal_ticks": tick(clip["duration_ms"]),
            "loop": key in {"idle", "walk"},
            "keypose_sheet": target.relative_to(MOTION).as_posix(),
            "keyposes": [{"frame": idx, "start_ms": rows[idx]["start_ms"],
                          "nearest_tick": tick(rows[idx]["start_ms"]),
                          "image": f"frames/{key}/{idx:04d}.png", "pose": note} for idx, note in poses],
            "pose_cues": [{"frame": idx, "start_ms": rows[idx]["start_ms"],
                           "suggested_tick": tick(rows[idx]["start_ms"]),
                           "event": event, "basis": note} for idx, event, note in POSE_CUES.get(key, ())],
        }
    (MOTION / "keyposes.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(out, timing)


if __name__ == "__main__":
    main()
