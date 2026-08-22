execute as @e at @s on attacker if entity @s[scores={chainsaw=0..},tag=rpg.h.chainsaw_tag1] store result score @s random run random value 1..5
execute as @e at @s on attacker if entity @s[scores={chainsaw=0..},tag=rpg.h.chainsaw_tag1] run summon evoker_fangs ~ ~ ~ {Motion:[0d,0.2d,0d],Health:10,Glowing:1b,attributes:[{id:"scale",base:3f},{id:"max_health",base:10f}]}
execute as @e at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run particle trial_spawner_detection ~0.25 ~1.25 ~0.25 -0.5 -0.5 -0.5 0.1 5
execute as @e at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run damage @e[limit=1,sort=nearest] 1 minecraft:player_attack
execute as @e at @s on attacker if entity @s[tag=rpg.h.chainsaw_tag1] run effect give @e[limit=1,sort=nearest] minecraft:glowing 1 1 true
scoreboard players reset * random
scoreboard players reset * chainsaw