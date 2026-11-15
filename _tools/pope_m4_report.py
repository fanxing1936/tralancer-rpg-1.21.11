"""汇总已完成的教皇 M4 证据；不会运行构建、改模型或同步实例。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "_tools/pope_ref"
OUT = REF / "m4"


def read(name):
    return json.loads((OUT / name).read_text("utf-8"))


def main():
    integration = read("integration/integration_validation.json")
    build = read("build/build_results.json")
    smoke = read("server_smoke/server_test_result.json")
    runtime = read("runtime/report.json")
    install = read("install_plan.json")
    model_hash = hashlib.sha256((REF / "pope.bbmodel").read_bytes()).hexdigest()
    assert integration["all_passed"] and build["all_passed"] and smoke["ok"] and runtime["functional_success"]
    assert model_hash == integration["model_sha256"] == runtime["model_sha256"]
    snapshot = Path(build["snapshot"])
    assert (snapshot / "_tools/add_pope_model.py").read_bytes() == (ROOT / "_tools/add_pope_model.py").read_bytes()
    assert (snapshot / "_tools/pope_ref/pope.bbmodel").read_bytes() == (REF / "pope.bbmodel").read_bytes()
    assert str(snapshot / "rpg") == runtime["datapack_source"]
    generator_hash = hashlib.sha256((ROOT / "_tools/add_pope_model.py").read_bytes()).hexdigest()
    released = {"attack": "0.50 秒 / 第 10 tick", "summon": "0.65 秒 / 第 13 tick", "cast": "0.90 秒 / 第 18 tick"}
    rows = []
    for clip in integration["clips"]:
        rows.append("| {id} | `{name}` | {seconds:.2f} | {ticks} | {frames} | {release} |".format(
            **clip, release=released.get(clip["name"], "—")))
    checks = []
    for step in build["steps"]:
        checks.append(f"| `{step['name']}` | 退出 {step['exit_code']}，{step['seconds']:.2f} 秒 | [日志](build/{step['name']}.log) |")
    report = f"""# 教皇 M4 接入与验证

模型接口、资源生成与专用服务器验证已完成。保留已确认的 B 眼神。**未在真实游戏内看过**；真实客户端视觉、插值、音效听感仍待验收，没有用构建通过代替外形还原判断。

- 事实来源：[pope.bbmodel](../pope.bbmodel)，SHA-256 `{model_hash}`。
- 薄配置：[add_pope_model.py](../../add_pope_model.py)，SHA-256 `{generator_hash}`。
- 12 个 item_display、44 个元素、170 个有效面；一张 128×64 base64 内嵌图集，原本体 64×64 像素原样复用。静态 model_scale `1.3593362401199063`，最高点约 2.6 格。
- 卫道士载体 `rpg.pope`，计分板前缀 `rpg_pp`，初始/最大血量 1000；summon 只有一条召唤命令。其他战斗属性交给玩法，不含 AI 状态机、伤害、掉落或特效生成。
- `build.sh`：tower_wraith → pope_model → 后续模型 → pope_fight；`rp_build.sh` 紧接 tower_guard。
- 主工作区仅生成教皇自己的 {integration['generated_file_count']} 个文件并合并 5 个共享注册文件；README 素材署名已更新。

## 动作与玩法接口

调用：以载体为执行者执行 `function rpg:pope/anim/enter/<clip>`。同一时间只播一段；idle/walk 循环，其余播完自动回 idle。idle 每 4 tick 采样，其余每 tick 采样，STRIDE=4 未改。

| ID | clip | 秒 | tick | 烘焙帧数 | 出手约定 |
|---:|---|---:|---:|---:|---|
{chr(10).join(rows)}

出手时间是本项目根据姿态制定的接口约定，不是从 GIF 恢复的原作事件。enter 立即播放 f0，此时 `rpg_pp_t=1`；fN 对应 score=N+1。非循环末帧后的下一刻回 idle。attack 只有一个推杖出手动作，三连弹的发射次数由玩法决定。

[sockets.json](../sockets.json) 含 idle、全部出手时刻及额外采样，共 525 个时间点×4挂点。`staff_tip` 是杖头发光立方体中心，`head_top` 跟随头顶、不跟随脱落皇冠；Minecraft `^左 ^上 ^前` 数值为 `[-x,y,-z]*model_scale/16`，相对载体脚底，不减 seat。座高另由专服验证为 2.0 格。

## 声音与载体运行

17 组 39 个原 OGG 逐字节复制，资源名仅按管线转换小写及下划线。M3 [audio_cues.json](../m3/audio_cues.json) 的 sounds/cues/enter_cues 直接用于配置：attack10、summon13、cast18 tick 出手声音；appear/teleport_in/teleport_out/whirlwind 各自 enter 时播放。

hurt 仍用现有 rpg.hurt 门控。ambient=0.006/刻是本项目配置选择，不宣称原作频率。magic_impact、三组 intro 及其他没有可靠动作事件的声音仅注册；whirlwind 不作为死亡回调。原声音不裁剪或变速，切动作不自动停止长尾，whirlwind 声音约13.033秒而动作7秒。

模型 tick 在 command/tick_end 前更新，tick_late 在其后恢复隐身。三个原版维度分别更新、清理，选择器均使用 distance=0.. 限定当前维度。未改 display_mob.py、DEVIL_SMOKE、STRIDE 或 rpg.hurt。

## 构建和真实服务端证据

完整构建在全新隔离副本运行，未在共享工作区执行会删除并重建 rpg 的 build.sh。最终快照：`{snapshot}`。

| 检查 | 结果 | 证据 |
|---|---|---|
{chr(10).join(checks)}
| 原始 server_test.py，完整包 | Done、数据包启用，无函数加载/命令错误 | [详细结果](server_smoke/server_test_result.json) |
| 模型专用真实服运行 | {runtime['passed']}/{len(runtime['checks'])} 项通过，无函数/命令错误 | [详细结果](runtime/report.json) |
| 主区重复生成 | 2 次逐字节一致 | [生成校验](integration/integration_validation.json) |
| 工作区保护 | {integration['protected_file_count']} 个文件字节不变；共享索引非教皇条目不变 | [基线](integration/protected_before.json) |

运行时检查包含 1000 血量、12 部件、实际座高、九段编号/时间/首中末帧的实际实体 NBT、非循环回 idle、四实例跨三个维度互不干扰、清除隐身后的恢复，以及只杀载体、等待死亡移除后 0 残留部件。检查的是服务器目标变换，**没有验证客户端插值图像**；清理结论限已加载区块。

完整包 smoke 没有删玩法入口。模型专项测试只在一次性测试副本中停用 pope_fight/tick 注册，所有玩法函数仍被解析，并给测试实体加 NoAI/NoGravity、使用冻结/步进来隔离物理与技能干扰；这些测试设置不进入交付生成器。仅豁免精确匹配的四条 localhost/offline 服务器环境提示，其余警告和错误完整保留。

专项测试还记录 **1 条 `Can't keep up` 性能警告（2301ms / 46 ticks behind）**，发生在任何教皇召唤前的首次异维度 forceload 准备阶段。155项功能断言均通过、函数/命令错误0、服务器正常退出；原始严格无额外告警判定仍为 false，另记 functional_success=true。没有删除该警告，也未重新测试来掩盖它；这不是持续负载性能基准。详见[运行时说明](runtime/RUNTIME_REVIEW.md)。

首轮专服发现三维度包装的无距离 @e 会跨维度选中实体，导致动画每刻推进三次。已在教皇入口修复并以新快照重新完整构建、重跑专服；[首次失败及诊断](runtime/attempt1_threefold_tick/diagnosis.json) 保留，未将首次失败写成通过。

## 玩法会话待对齐（本次未修改）

当前玩法脚本仍使用占位时序，详见[独立审计](INDEPENDENT_PREINTEGRATION_AUDIT.md)：

| 项目 | 模型约定 | 现有玩法 | 需要对齐的影响 |
|---|---:|---:|---|
| attack 结束 | 25 tick | 24 tick | 提前一刻切换 |
| summon 出手 | 13 tick | 20 tick | 比姿态/音效晚7刻 |
| cast 出手/结束 | 18 / 50 tick | 部分技能40tick生效并结束 | 出手和末段不一致 |
| appear 结束 | 36 tick | 40 tick | 先回 idle 等待 |
| whirlwind 收拢 | 140 tick | 60 tick移除载体 | 截去后4秒及收拢姿态 |

`_tools/add_pope_fight.py`、`rpg:pope_fight/`、`docs/POPE-DESIGN.md` 均未改。隔离完整构建已让玩法生成器识别模型；主工作区的原玩法产物按边界保留，原 clip 包装中的占位注释由玩法会话下次生成处理。本任务不声称完整 Boss 战已经验收。

## 视觉与同步边界

视觉依据仍是已经交付的 [M2静态对照](../M2_REVIEW.md) 与 [M3九段动作对照](../m3/index.html)。瞬移没有透明度/缩放；旋风6.4～7秒收拢为项目推断，刚性部件体积不会缩小；必须由玩法在回 idle 前接走。原作发光色周期/半透明/旋风特效没有制作，详见 M3 报告。

本次未同步测试实例、未提交、未推送。已只读准备[同步计划](install_plan.json)：目标存档“{install['world']}”，{install['counts']['add']} 个教皇新文件＋{install['counts']['merge']} 个共享索引合并，共 {install['pending_writes']} 个计划写入；不更改玩法或其他怪物。计划需要用户明确批准后才能执行，执行前须复核目标哈希并备份。

[游戏内调试命令](DEBUG_COMMANDS.md)。**未在真实游戏内看过。**
"""
    (OUT / "M4_REPORT.md").write_text(report, "utf-8")
    commands = """# 教皇模型调试命令

这些命令用于已同步模型的数据包与资源包。当前尚未同步测试实例。只测试模型，不启动 pope_fight。

1. 重载数据包 `/reload`，资源包用 F3+T 重载。
2. 在空地召唤 `/function rpg:pope/summon`。自然卫道士有原版行为；下面的 NoAI/NoGravity 只作手动模型审阅夹具，不属于生成器或战斗设计。

```mcfunction
/execute as @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] run data merge entity @s {NoAI:1b,NoGravity:1b}
/execute as @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] at @s run function rpg:pope/anim/enter/attack
```

把最后的 attack 换成 idle、walk、summon、cast、appear、teleport_in、teleport_out、whirlwind 即可。walk 只在载体移动时保持循环；静止时共用位移监测会在下一次检测后切回 idle。需要四面看头眼、肩臂、袍背、皇冠和权杖；特别检查 attack 杖头近地处、cast 浮动杖头、whirlwind 掉冠脱手及7秒末姿。

读取当前动画编号、计数器及部件：

```mcfunction
/scoreboard players get @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] rpg_pp_anim
/scoreboard players get @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] rpg_pp_t
/data get entity @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16,sort=nearest,limit=1] Passengers
```

单独测试声音（其余事件见 sounds.json 的 pope.*）：

```mcfunction
/playsound rpg:pope.spell hostile @s ~ ~ ~ 1 1
/stopsound @s hostile rpg:pope.whirlwind
```

清理测试：只杀附近教皇载体，等待至少 2 秒，再检查附近部件。不要先杀部件，否则无法检验孤儿清理。

```mcfunction
/kill @e[type=minecraft:vindicator,tag=rpg.pope,distance=..16]
/execute unless entity @e[type=minecraft:item_display,tag=rpg.pope.part,distance=..32] run say 教皇部件已清理
```

服务端已验证主世界、下界、末地的已加载区块；客户端仍须真实截图核对。瞬移不会自行透明/消失，旋风也不会自行变成末影之心，均由玩法后续交接。
"""
    (OUT / "DEBUG_COMMANDS.md").write_text(commands, "utf-8")
    summary = {"model_sha256": model_hash, "generator_sha256": generator_hash,
               "build_all_passed": True, "server_smoke_passed": True,
               "runtime_passed": runtime["passed"], "runtime_checks": len(runtime["checks"]),
               "runtime_functional_success": runtime["functional_success"],
               "runtime_strict_success": runtime["success"],
               "runtime_extra_warnings": len(runtime.get("unexpected_warnings", [])),
               "workspace_protected_files": integration["protected_file_count"],
               "client_sync_performed": False, "in_game_visual_verified": False,
               "gameplay_timing_alignment_pending": True}
    (OUT / "delivery_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
