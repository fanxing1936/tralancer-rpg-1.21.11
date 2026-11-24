execute if score @s rpg_fo_fe <= #now rpg_fo run return run scoreboard players set @s rpg_fo_fe 0
particle minecraft:dust{color:[0.2,0.25,0.06],scale:0.5} ~ ~1.2 ~ 5 1 5 0 160
playsound minecraft:entity.bee.loop_aggressive player @a[distance=..16] ~ ~ ~ 0.6 0.4
scoreboard players set #dmg rpg_fo 30
scoreboard players set #hm rpg_fo 10
tag @s add rpg.fo.me
execute store result score #n rpg_fo if entity @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..8]
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..8] at @s run function rpg:force/hit
tag @s remove rpg.fo.me
execute if score #n rpg_fo matches 2.. run effect give @s minecraft:instant_health 1 0 true
execute if score #n rpg_fo matches 1 run effect give @s minecraft:regeneration 2 1 true
