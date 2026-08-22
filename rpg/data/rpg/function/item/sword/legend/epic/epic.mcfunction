execute as @e at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run effect give @s minecraft:fire_resistance 2 3
execute as @e at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run particle dust_color_transition{from_color:[1.0,0.84,0.0],to_color:[1.0,0.64,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * sun

execute as @e at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run effect give @e[distance=..1,limit=1] minecraft:slowness 2 255 true
execute as @e at @s on attacker if entity @s[tag=rpg.h.ice_tag1] run damage @e[distance=..1,limit=1] 1 freeze
execute as @e at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run particle dust_color_transition{from_color:[0.58,0.92,1.0],to_color:[1.0,1.0,1.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * ice

execute as @e at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run effect give @s minecraft:resistance 2 0
execute as @e at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run particle dust_pillar{block_state:{Name:iron_block}} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
scoreboard players reset * steel

execute as @e at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run effect give @e[distance=..1,limit=1] minecraft:wither 2 3 true
execute as @e at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run effect give @e[distance=..1,limit=1] minecraft:glowing 2 3 true
execute as @e at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3} ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 30
execute as @e at @s on attacker if entity @s[tag=rpg.h.sea_tag1] run particle raid_omen ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 3
scoreboard players reset * sea


execute as @a[scores={ice_step=45..}] anchored eyes at @s run playsound minecraft:entity.player.hurt_freeze player @s
execute as @a[scores={ice_step=45..}] anchored eyes at @s run data merge entity @e[distance=0.1..5,limit=1,sort=arbitrary,type=!item] {Motion:[0d,2.5d,0d]}
execute as @a[scores={ice_step=45..}] anchored eyes at @s at @e[distance=0.1..5] run particle dust_pillar{block_state:{Name:blue_ice}} ~0.5 ~1 ~0.5 -1 -1 -1 1 10
execute as @a[scores={ice_step=50..}] anchored eyes at @s run scoreboard players set @s ice_step 0


execute as @a[scores={sea_step=10..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"sea_atk"}],Invulnerable:1b}
execute as @a[scores={sea_step=10..}] anchored eyes at @s run playsound minecraft:weather.rain player @s
execute as @e[name=sea_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={sea_step=10..}]
execute as @a[scores={sea_step=10..}] anchored eyes at @s run scoreboard players set @s sea_step 0
execute as @e[name=sea_atk,type=armor_stand] anchored eyes at @s run particle dust_color_transition{from_color:[1.0,0.38,0.92],to_color:[1.0,0.78,0.0],scale:3} ~0.125 ~0.5 ~0.125 -0.25 -0.25 -0.25 0.1 20
execute as @e[name=sea_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=sea_atk,type=armor_stand] anchored feet at @s as @e[distance=0.1..1.5] run damage @s 5 minecraft:drown