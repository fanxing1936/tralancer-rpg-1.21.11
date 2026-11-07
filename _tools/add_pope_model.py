# -*- coding: utf-8 -*-
"""教皇外观：pope.bbmodel -> 12 个展示部件、九段动作和原作音效。

只负责模型载体与动画；战斗由 add_pope_fight.py 的独立会话维护。
模型和动作的事实来源为 pope_ref/pope.bbmodel；不运行制作/拟合脚本。
音效绑定沿用 M3 审阅清单，长尾原音不裁剪、不随动作结束自动截断。
"""
import json
import os
import sys

from display_mob import Mob, build, hook_tag, passenger, wf, wj, write_rig_runtime

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "pope_ref")
RP = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
DP = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
MAX_HEALTH = 1000
DIMENSIONS = ("overworld", "the_nether", "the_end")

with open(os.path.join(REF, "m3", "audio_cues.json"), encoding="utf-8") as fh:
    AUDIO = json.load(fh)

MOB = Mob(
    key="pope", label="教皇", generator="add_pope_model.py",
    bbmodel=os.path.join(REF, "pope.bbmodel"),
    parts=[
        ("body", ["body", "chain_right", "chain_left"]),
        ("head", ["head", "right_brow", "left_brow"]),
        ("crown", ["crown"]),
        ("right_arm", ["right_arm"]),
        ("right_hand", ["right_hand"]),
        ("left_arm", ["left_arm"]),
        ("left_hand", ["left_hand"]),
        ("right_leg", ["right_leg"]),
        ("left_leg", ["left_leg"]),
        ("cape", ["cape"]),
        ("staff", ["staff"]),
        ("staff_glow", ["staff_glow"]),
    ],
    glow={"staff_glow"},
    # 普通卫道士座高 2 格；静态最高点 30.60317144 模型单位 -> 2.6 格。
    seat=2.0, model_scale=1.3593362401199063,
    tag="rpg.pope", score="rpg_pp", carrier="minecraft:vindicator",
    # 顺序即玩法接口 ID。动作每刻采样，0.65 秒 cue 落在第 13 刻。
    clips=[
        ("idle", 4, True),
        ("walk", 1, True),
        ("attack", 1, False),
        ("summon", 1, False),
        ("cast", 1, False),
        ("appear", 1, False),
        ("teleport_in", 1, False),
        ("teleport_out", 1, False),
        ("whirlwind", 1, False),
    ],
    sounds=AUDIO["sounds"],
    sound_dir=os.path.join(REF, "sounds"),
    cues=AUDIO["cues"], enter_cues=AUDIO["enter_cues"],
    hurt="hurt", ambient=("idle", 0.006),
    # whirlwind 不是死亡音；不在部件清理时重播。
)


def write_datapack(rest):
    passengers = ",".join(passenger(MOB, part, comp) for part, comp in rest)
    wf(os.path.join(MOB.func, "summon.mcfunction"), [
        "# 教皇模型载体与十二个展示部件。由 add_pope_model.py 生成。",
        "# 此函数只召唤；其余战斗属性、AI、技能及阶段切换归玩法层。",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.pope"],Silent:1b,'
        'PersistenceRequired:1b,CanPickUpLoot:0b,Health:%df,'
        'CustomName:[{text:"教皇",color:"#E3B04B",bold:true}],'
        'active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}],'
        'attributes:[{id:"minecraft:max_health",base:%df}],Passengers:[%s]}'
        % (MAX_HEALTH, MAX_HEALTH, passengers),
    ])
    write_rig_runtime(MOB, [
        "# 当前维度：载体跟随、动画与音效；共用管线在末尾清理孤儿部件。",
        "execute if entity @e[type=minecraft:vindicator,tag=rpg.pope,limit=1] "
        "as @e[type=minecraft:vindicator,tag=rpg.pope] at @s run function rpg:pope/follow",
    ])
    # #minecraft:tick 默认主世界上下文；只在自己的入口分发三个原版维度。
    # 没有空间限制的 @e 会跨维度选实体，必须同时限定载体和孤儿扫描。
    # 仅处理本生成器刚写出的入口，保持 display_mob 与其他怪物不变。
    with open(os.path.join(MOB.func, "tick.mcfunction"), encoding="utf-8") as fh:
        dimension_lines = fh.read().replace("@e[", "@e[distance=0..,").splitlines()
    wf(os.path.join(MOB.func, "tick_dimension.mcfunction"), dimension_lines)
    wf(os.path.join(MOB.func, "tick.mcfunction"), [
        "# 三个原版维度均更新动画并清理无载体的教皇部件。",
    ] + ["execute in minecraft:%s run function rpg:pope/tick_dimension" % d
         for d in DIMENSIONS])
    wj(os.path.join(MOB.dp, "data", "rpg", "predicate", "pope", "invisible.json"), {
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"effects": {"minecraft:invisibility": {}}},
    })
    wf(os.path.join(MOB.func, "tick_late.mcfunction"), [
        "# 参照亚巴顿：在 command/tick_end 之后恢复载体隐身，不改显形/受伤逻辑。",
    ] + ["execute in minecraft:%s as @e[distance=0..,type=minecraft:vindicator,tag=rpg.pope] "
         "unless predicate rpg:pope/invisible run effect give @s minecraft:invisibility infinite 0 true" % d
         for d in DIMENSIONS])
    hook_tag(MOB.dp, "tick", "rpg:pope/tick_late", False)


def main():
    _, rest = build(MOB, RP, DP)
    write_datapack(rest)


if __name__ == "__main__":
    main()
