scoreboard players operation #dd rpg_fo = @s rpg_fo_d2
scoreboard players set @s rpg_fo_d2 0
execute unless score @s rpg_ident matches 4..5 unless score @s rpg_pillar matches 1 run return 0
execute store result score #ph rpg_fo run data get entity @s Health 10
scoreboard players set #pct rpg_fo 0
tag @s add rpg.fo.me
execute as @e[tag=rpg.hurt,type=!minecraft:player,distance=..8,limit=1,sort=nearest] at @s run function rpg:force/x/id/dealt_on
tag @s remove rpg.fo.me
