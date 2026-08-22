# 由 opt_invert.py 内外翻：原本这 8 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] store result score @s random run random value 1..5
execute at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d,0d]}
execute at @s on attacker if entity @s[scores={montain=0..},tag=rpg.h.montain_tag1] run particle gust ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.15,0.91,0.76],to_color:[0.9,0.63,0.0],scale:2} ~0.1 ~0.7 ~0.1 -0.2 -0.5 -0.2 0.1 5
execute at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run particle dust_color_transition{from_color:[0.9,0.63,0.0],to_color:[0.15,0.91,0.76],scale:1} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 2
execute at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack by @s
execute at @s on attacker if entity @s[tag=rpg.h.montain_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
