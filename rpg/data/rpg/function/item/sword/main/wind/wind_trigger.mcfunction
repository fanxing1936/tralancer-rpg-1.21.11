# 加上握持判定：原本没有这一条，攒满任何一块符石都会把三种效果一起放出。
execute as @a[tag=rpg.h.wind_tag1,scores={wind=50..}] anchored feet at @s run summon armor_stand ^ ^ ^2 {Invisible:1b,CustomName:[{"text":"wind_atk"}],Invulnerable:1b}
execute as @a[tag=rpg.h.wind_tag1,scores={wind=50..}] anchored eyes at @s run playsound minecraft:entity.breeze.wind_burst player @s
execute as @e[name=wind_atk,type=armor_stand] at @s run tp @s ~ ~ ~ facing entity @p[scores={wind=50..}]
execute as @a[tag=rpg.h.wind_tag1,scores={wind=50..}] anchored eyes at @s run scoreboard players set @s wind 0
execute as @e[name=wind_atk,type=armor_stand] anchored eyes at @s run particle gust ~0.25 ~0.5 ~0.25 -0.5 -0.5 -0.5 1 20

execute as @e[name=wind_atk,type=armor_stand] anchored feet at @s run tp @s ^ ^ ^-1  
execute as @e[name=wind_atk,type=armor_stand] anchored feet at @s as @e[distance=0.1..1.5] run damage @s 17 minecraft:wind_charge