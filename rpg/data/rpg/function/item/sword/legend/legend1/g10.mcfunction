# 8 行原本各自扫一遍全实体表找 @e[tag=rpg.hurt]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] store result score @e[limit=1,sort=nearest] random run random value 1..5
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,distance=0.1..2] 2 minecraft:player_attack by @s
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run damage @e[limit=1,sort=nearest] 2 minecraft:player_attack by @s
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run effect give @e[distance=0..2] wither 5 1 true
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run particle sculk_soul ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={soul=0..},tag=rpg.h.soul_tag1] run particle trial_spawner_detection_ominous ~0.25 ~1.2 ~0.25 -0.5 -1 -0.5 0.1 50
