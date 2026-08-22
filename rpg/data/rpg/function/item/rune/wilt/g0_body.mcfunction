# 由 opt_invert.py 内外翻：原本这 6 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[tag=rpg.h.wilt_tag1] run scoreboard players set @s rpg_rune_roll 0
execute at @s on attacker if entity @s[tag=rpg.h.wilt_tag1] store result score @s rpg_rune_roll run random value 1..4
execute at @s on attacker if entity @s[tag=rpg.h.wilt_tag1,scores={rpg_rune_roll=1}] run tag @s add rpg.rune.wilt
execute at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run effect give @s minecraft:wither 5 1 true
execute at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run particle dust_color_transition{from_color:[0.16,0.16,0.16],to_color:[0.05,0.22,0.05],scale:2} ~ ~1 ~ 0.3 0.5 0.3 0.04 24
execute at @s if entity @a[tag=rpg.rune.wilt,distance=..8] run playsound minecraft:entity.wither.shoot hostile @a[distance=..16] ~ ~ ~ 0.5 1.6
