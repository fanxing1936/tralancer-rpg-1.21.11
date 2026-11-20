# -*- coding: utf-8 -*-
"""疯人王扫罗的外观（docs/SAUL-DESIGN.md）：原作玩家英雄网格、织网者皮肤、坚毅铠甲，手持千刀。

    python add_saul_model.py ../resourcepack ../rpg

模型在 _tools/saul_dungeons_ref/（dungeons_models.py 的 saul）：
  身体   SK_Player_Master，材质换成织网者 T_Spider_Skin（wiki 的 Web Crawler）
  盔甲   坚毅铠甲（强化锁甲的独特变体）六件，挂在玩家骨架的护甲插槽上，贴图 T_StalwartArmor
  武器   千刀：一代细剑 SM_Rapier，贴图按千刀配色重画（saul_boss_ref/make_thousand_cuts.py），右手武器插槽
动作全是原作玩家动作（武士刀待机/行走/奔跑、细剑连招、翻滚、表情等）。
换装对象：带 rpg.slwear 的实体（扫罗战的载体 rpg.slb）。
碎甲：rpg:saul/armor/{full,broken}；broken 把头盔、左臂甲（连护肩）换成空模型，并在原处抛出两块碎甲落地。
对着空气练剑时对面的老战友：saul_ghost（原作英雄默认皮肤，转成半透明的白），载体 rpg.slg。
"""
import os
import sys

from display_mob import wf
from lord_look import LordLook

HERE = os.path.dirname(os.path.abspath(__file__))
BROKEN = ("helmet", "l_pauldron")        # 二阶段碎掉的甲（左臂甲原作就连着护肩，是一件）


def ev(*ids):
    return ["minecraft:" + i for i in ids]


# 原作细剑与坚毅铠甲的音效只在本体里（导出器导不出音频），先用原版声音
SOUNDS = {
    "hurt": (("扫罗：受伤", "Saul hurts"), ev("entity.player.hurt")),
    "death": (("扫罗：倒下", "Saul falls"), ev("entity.player.death")),
    "stab": (("千刀：刺击", "The Thousand Cuts stabs"), ev("entity.player.attack.sweep")),
    "stab2": (("千刀：快刺", "The Thousand Cuts strikes"), ev("entity.player.attack.strong")),
    "final": (("千刀：收剑", "The Thousand Cuts finishes"), ev("entity.player.attack.knockback")),
    "roll": (("扫罗：翻滚", "Saul rolls"), ev("entity.player.attack.nodamage")),
    "step": (("扫罗：甲胄脚步", "Armoured steps"), ev("block.chain.step")),
    "laugh": (("扫罗：大笑", "Saul laughs"), ev("entity.witch.celebrate")),
}

LOOK = LordLook(
    key="saul", lord=0, label="扫罗", tag="rpg.slm", generator="add_saul_model.py",
    carriers="tag=rpg.slwear", carrier_type=None,
    clips=[("idle", 4, True), ("walk", 2, True), ("run", 2, True),
           ("thrust", 1, False), ("left", 1, False), ("right", 1, False), ("double", 1, False), ("final", 1, False),
           ("roll_f", 1, False), ("roll_b", 1, False), ("roll_l", 1, False), ("roll_r", 1, False),
           ("mighty", 2, False), ("twirl", 2, False), ("shadow", 2, False), ("kneel", 2, False), ("hero", 2, False),
           ("web", 1, False), ("showoff", 1, False), ("vanish", 1, False), ("land", 1, False),
           ("stun", 2, True), ("hurt", 1, False), ("fall", 1, False), ("down", 2, True)],
    sounds=SOUNDS,
    cues={"walk": [(0.0, "step", 0.3, 1.0), (2.1, "step", 0.3, 1.0)],
          "run": [(0.2, "step", 0.3, 1.1), (1.1, "step", 0.3, 1.1)],
          "thrust": [(0.08, "stab", 1.0, 1.3)], "left": [(0.05, "stab2", 1.0, 1.4)], "right": [(0.05, "stab2", 1.0, 1.3)],
          "double": [(0.05, "stab2", 1.0, 1.4), (0.2, "stab2", 1.0, 1.5)], "final": [(0.3, "final", 1.0, 1.1)],
          "roll_f": [(0.1, "roll", 0.8, 0.9)], "roll_b": [(0.1, "roll", 0.8, 0.9)],
          "roll_l": [(0.1, "roll", 0.8, 0.9)], "roll_r": [(0.1, "roll", 0.8, 0.9)]},
    skills={}, arrive="hero",
)
MOB = LOOK.mob

GHOST = LordLook(
    key="saul_ghost", lord=0, label="老战友的幻影", tag="rpg.slgm", generator="add_saul_model.py",
    carriers="type=minecraft:vindicator,tag=rpg.slg",
    clips=[("idle", 4, True), ("walk", 2, True), ("shadow", 2, False), ("thrust", 1, False), ("final", 1, False), ("roll_f", 1, False)],
    sounds={"swish": (("幻影挥剑", "A phantom blade"), ev("entity.player.attack.sweep"))},
    cues={"shadow": [(0.6, "swish", 0.5, 1.6), (1.6, "swish", 0.5, 1.5), (2.6, "swish", 0.5, 1.7)]},
    skills={}, arrive="idle",
)


def armour(dp):
    """rpg:saul/armor/full | broken (as carrier)."""
    func = os.path.join(dp, "data", "rpg", "function", "saul")
    full = ["# 全身甲（as 载体）。由 add_saul_model.py 生成。"]
    broken = ["# 碎甲（as/at 载体）：头盔、左臂甲换成空模型，并在原处抛出碎甲。由 add_saul_model.py 生成。"]
    for p in BROKEN:
        full.append('execute on passengers if entity @s[tag=rpg.slm.p.%s] run data modify entity @s '
                    'item.components."minecraft:item_model" set value "rpg:saul/%s"' % (p, p))
        broken += [
            # 碎甲：同一个物品模型、同一个变换，召在部件当前的位置，之后由 rpg:saul_boss 抛出、落地
            'execute on passengers if entity @s[tag=rpg.slm.p.%s] at @s run summon minecraft:item_display ~ ~ ~ '
            '{Tags:["rpg.slb.fx","rpg.slb.shard","rpg.slb.shardnew","rpg.slb.shard.%s"],item:{id:"minecraft:paper",count:1,'
            'components:{"minecraft:item_model":"rpg:saul/%s"}},item_display:"none",teleport_duration:3,interpolation_duration:3,'
            'view_range:1.5f}' % (p, p, p),
            'execute on passengers if entity @s[tag=rpg.slm.p.%s] run data modify entity @e[type=minecraft:item_display,'
            'tag=rpg.slb.shardnew,limit=1,sort=nearest] transformation set from entity @s transformation' % p,
            'execute on passengers if entity @s[tag=rpg.slm.p.%s] run data modify entity @e[type=minecraft:item_display,'
            'tag=rpg.slb.shardnew,limit=1,sort=nearest] Rotation set from entity @s Rotation' % p,
            'tag @e[type=minecraft:item_display,tag=rpg.slb.shardnew] remove rpg.slb.shardnew',
            'execute on passengers if entity @s[tag=rpg.slm.p.%s] run data modify entity @s '
            'item.components."minecraft:item_model" set value "rpg:empty"' % p,
        ]
    wf(os.path.join(func, "armor", "full.mcfunction"), full)
    wf(os.path.join(func, "armor", "broken.mcfunction"), broken)
    wf(os.path.join(func, "debug", "preview.mcfunction"), [
        "# 预览扫罗的外观：一个站着不动的载体（不是战斗）。清掉用 /function rpg:saul/debug/clear",
        'summon minecraft:vindicator ~ ~ ~ {Tags:["rpg.slb","rpg.slwear","rpg.slb.preview"],NoAI:1b,Silent:1b,PersistenceRequired:1b,'
        'Invulnerable:1b,active_effects:[{id:"invisibility",duration:-1,amplifier:0,show_particles:0b}]}',
    ])
    wf(os.path.join(func, "debug", "clear.mcfunction"), [
        "execute as @e[type=minecraft:vindicator,tag=rpg.slb.preview] run function rpg:saul/debug/clear_one"])
    wf(os.path.join(func, "debug", "clear_one.mcfunction"), ["execute on passengers run kill @s", "tp @s ~ -256 ~", "kill @s"])
    for clip, *_r in MOB.clips:
        wf(os.path.join(func, "debug", "play", clip + ".mcfunction"), [
            "execute as @e[tag=rpg.slm,limit=1,sort=nearest] run function rpg:saul/anim/enter/%s" % clip])


def ghost(rp):
    """The phantom's atlas -> a pale blue-white, half transparent (partial alpha works on item models)."""
    from PIL import Image
    import numpy as np
    path = os.path.join(rp, "assets", "rpg", "textures", "item", "saul_ghost", "atlas.png")
    a = np.array(Image.open(path).convert("RGBA")).astype(float)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255.0
    seen = a[..., 3] > 0
    t = 0.55 + 0.45 * lum
    a[..., 0], a[..., 1], a[..., 2] = 232 * t, 236 * t, 246 * t
    a[..., 3] = np.where(seen, 130, 0)
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(path)


if __name__ == "__main__":
    rp = sys.argv[1] if len(sys.argv) > 1 else "../resourcepack"
    dp = sys.argv[2] if len(sys.argv) > 2 else "../rpg"
    LOOK.main(rp, dp)
    armour(dp)
    GHOST.main(rp, dp)
    ghost(rp)
    print("saul look: %d parts; broken armour %s" % (len(MOB.parts), ", ".join(BROKEN)))
