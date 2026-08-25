
execute if entity @s[tag=rpg.boss.minion2] run scoreboard players add @s rpg_boss_fx 1
execute if entity @s[tag=rpg.boss.minion2,scores={rpg_boss_fx=1200..}] run return run kill @s
execute if entity @s[tag=rpg.boss.minion2] unless entity @e[type=minecraft:vindicator,tag=devil2,tag=boss,limit=1] run return run kill @s
execute if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute if entity @s[tag=boss] run function rpg:entities/warden/phase2_boss
