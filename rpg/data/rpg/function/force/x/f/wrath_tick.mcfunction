execute if score @s rpg_fo_wr <= #now rpg_fo run return run scoreboard players set @s rpg_fo_wr 0
particle minecraft:dust{color:[1.0,0.36,0.32],scale:0.8} ~ ~1 ~ 0.3 0.6 0.3 0 1
execute unless score @s rpg_fo_dt matches 1.. run return 0
scoreboard players set @s rpg_fo_dt 0
playsound minecraft:entity.blaze.shoot player @a[distance=..16] ~ ~ ~ 1 0.6
particle minecraft:flame ~ ~1 ~ 2 0.5 2 0.05 60
particle minecraft:dust{color:[0.48,0.85,0.3],scale:1.2} ~ ~1 ~ 2 0.5 2 0 30
scoreboard players set #dmg rpg_fo 40
scoreboard players set #hm rpg_fo 10
tag @s add rpg.fo.me
execute as @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..4] at @s run function rpg:force/hit
effect give @e[type=#rpg:seal_hostile,tag=!rpg.ally,distance=..4] minecraft:poison 3 1 true
tag @s remove rpg.fo.me
