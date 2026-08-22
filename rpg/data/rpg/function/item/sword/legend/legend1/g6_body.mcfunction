# 由 opt_invert.py 内外翻：原本这 5 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={potion=0..},tag=rpg.h.potion_tag1] store result score @s random run random value 1..5
execute at @s on attacker if entity @s[scores={potion=0..},tag=rpg.h.potion_tag1] run summon llama_spit ~ ~5 ~ {Motion:[0d,-1d,0d]}
execute at @s on attacker if entity @s[scores={potion=0..},tag=rpg.h.potion_tag1] run particle crit ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.5 30
execute at @s on attacker if entity @s[tag=rpg.h.potion_tag1] run particle dust_color_transition{from_color:[0.52,0.8,0.0],to_color:[0.98,0.98,0.98],scale:2} ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 3
execute at @s on attacker if entity @s[tag=rpg.h.potion_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
