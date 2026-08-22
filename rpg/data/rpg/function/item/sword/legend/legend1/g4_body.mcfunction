# 由 opt_invert.py 内外翻：原本这 5 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={chainsaw=0..},tag=rpg.h.chainsaw_tag1] store result score @s random run random value 1..5
execute at @s on attacker if entity @s[scores={chainsaw=0..},tag=rpg.h.chainsaw_tag1] run summon evoker_fangs ~ ~ ~ {Motion:[0d,0.2d,0d],Health:10,Glowing:1b,attributes:[{id:"scale",base:3f},{id:"max_health",base:10f}]}
execute at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run particle trial_spawner_detection ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack
execute at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
