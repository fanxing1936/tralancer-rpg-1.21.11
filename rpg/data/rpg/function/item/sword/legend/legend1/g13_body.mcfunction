# 由 opt_invert.py 内外翻：原本这 5 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] as @e[distance=0.1..2] at @s run damage @s 2 minecraft:player_attack
execute at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run effect give @e[distance=0..2] glowing 5 3 true
execute at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[1.0,1.0,1.0],scale:3} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 0.1 20
execute at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
execute at @s on attacker if entity @s[scores={power=0..},tag=rpg.h.power_tag1] run particle enchant ~0.25 ~1.2 ~0.25 -0.5 -0.75 -0.5 1 20
