# 由 opt_invert.py 内外翻：原本这 4 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[tag=rpg.h.chime_tag1] run tag @s add rpg.epic.chime
execute at @s if entity @a[tag=rpg.epic.chime,distance=..8] run particle dust_color_transition{from_color:4066619,to_color:11121336,scale:2} ~ ~1 ~ 0.4 0.5 0.4 0.05 24
execute at @s if entity @a[tag=rpg.epic.chime,distance=..8] run playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..16] ~ ~ ~ 1 1.2
execute at @s if entity @a[tag=rpg.epic.chime,distance=..8] run function rpg:item/epic/chime_wave
