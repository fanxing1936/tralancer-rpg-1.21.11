# 由 opt_invert.py 内外翻：原本这 8 行每行都自己扫一遍全实体表
# 找 @e[tag=rpg.hurt]。现在上层扫一次，行内一律对 @s 操作。
# 已静态验证过没有反向依赖，所以两种遍历顺序等价。

execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] store result score @e[limit=1,sort=nearest] random run random value 1..5
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,sort=nearest] 2 minecraft:player_attack by @s
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run effect give @e[distance=0..2] wither 5 1 true
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
