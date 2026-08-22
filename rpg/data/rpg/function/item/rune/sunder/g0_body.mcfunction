# 由 opt_invert.py 内外翻：原本这 5 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[tag=rpg.h.sunder_tag1] run tag @s add rpg.rune.sunder
execute at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run effect give @s minecraft:weakness 6 1 true
execute at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run effect give @s minecraft:glowing 6 0 true
execute at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run particle crit ~ ~1 ~ 0.35 0.4 0.35 0.25 18
execute at @s if entity @a[tag=rpg.rune.sunder,distance=..8] run playsound minecraft:item.shield.break hostile @a[distance=..14] ~ ~ ~ 0.6 1.4
