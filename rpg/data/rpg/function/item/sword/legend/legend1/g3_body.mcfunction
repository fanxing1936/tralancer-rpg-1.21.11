# 由 opt_invert.py 内外翻：原本这 4 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run effect give @e[distance=0..1] minecraft:wither 2 3 true
execute at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run effect give @e[distance=0..1] minecraft:glowing 2 3 true
execute at @s on attacker if entity @s[scores={blil=0..},tag=rpg.h.blil_tag1] run particle dust_color_transition{from_color:[0.4,0.0,0.6],scale:3,to_color:[0.0,0.0,0.0]} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute at @s on attacker if entity @s[tag=rpg.h.blil_tag1] run particle witch ~0.25 ~1.5 ~0.25 -0.5 -1 -0.5 0 2
