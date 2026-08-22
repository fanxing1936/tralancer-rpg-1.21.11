execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run effect give @e[distance=0..2] minecraft:wind_charged 20 40 true
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run particle dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:3} ~1 ~2 ~1 -2 -2 -2 1 50
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run particle minecraft:gust_emitter_small ~0.5 ~1.2 ~0.5 -1 -1 -1 1 2
execute as @e at @s on attacker if entity @s[scores={typhoon=0..},tag=rpg.h.typhoon_tag1] run data merge entity @e[limit=1,sort=nearest] {Motion:[0d,0.8d,0d]}
scoreboard players reset * typhoon

execute as @a[scores={typhoon_step=50..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"typhoon_atk"}],Invulnerable:1b}
execute as @a[scores={typhoon_step=50..}] anchored feet at @s run summon armor_stand ^2 ^ ^2 {Invisible:1b,CustomName:[{"text":"typhoon_atk"}],Invulnerable:1b}
execute as @a[scores={typhoon_step=50..}] anchored feet at @s run summon armor_stand ^-2 ^ ^2 {Invisible:1b,CustomName:[{"text":"typhoon_atk"}],Invulnerable:1b}

execute as @a[scores={typhoon_step=50..}] anchored eyes at @s run playsound minecraft:item.trident.throw player @s
execute as @e[name=typhoon_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={typhoon_step=50..}]
execute as @a[scores={typhoon_step=50..}] anchored eyes at @s run scoreboard players set @s typhoon_step 0
execute as @e[name=typhoon_atk,type=armor_stand] anchored eyes at @s run particle minecraft:gust_emitter_small ~0.5 ~1.2 ~0.5 -1 -1 -1 1 2 force
execute as @e[name=typhoon_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[0.53,0.78,0.37],to_color:[1.0,1.0,1.0],scale:3} ~1 ~2 ~1 -2 -2 -2 1 10 force
execute as @e[name=typhoon_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=typhoon_atk,type=armor_stand] anchored feet at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2.5] {Motion:[0d,2.5d,0d]}
execute as @e[name=typhoon_atk,type=armor_stand] anchored feet at @s unless entity @a[distance=..50,tag=rpg.h.typhoon_tag1] run kill 