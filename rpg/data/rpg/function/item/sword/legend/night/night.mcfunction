advancement revoke @s only rpg:item/night
execute as @s at @s if entity @s[tag=rpg.h.sakura_tag1] run particle enchant ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
execute as @s at @s unless entity @s[tag=rpg.h.sakura_tag1] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 10
execute as @s[scores={level=1..}] at @s run scoreboard players add @s night 1
execute if entity @s[tag=rpg.h.sakura_tag1] as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run particle dust_color_transition{from_color:[1.0,0.47,0.47],to_color:[1,1,1],scale:1} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 500
execute unless entity @s[tag=rpg.h.sakura_tag1] as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run particle dust_color_transition{from_color:[0.4,0.0,1.0],scale:1,to_color:[0.0,0.0,0.0]} ~0.5 ~0.5 ~0.5 -1 -1 -1 0.2 500
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 0 100
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run summon minecraft:tnt ~ ~ ~ {fuse:0s,explosion_power:1.0f,Silent:1b}
execute as @s[scores={level=1..,night=20..}] at @e[distance=0.1..5] run kill @e[type=#minecraft:arrows,distance=..3]
execute as @s[scores={level=1..,night=20..}] at @s run playsound minecraft:entity.ender_dragon.shoot player @s
execute as @s[scores={level=1..,night=20..}] at @s anchored eyes run xp add @s -3 points
execute as @s[scores={night=20..}] at @s run scoreboard players set @s night 0
