execute store result score #tod rpg_dm run time query daytime
execute unless score #tod rpg_dm matches 13000..23000 run return 0
execute as @a[tag=rpg.dm.job] at @s if entity @e[type=minecraft:marker,tag=rpg.tw.at.church,distance=..4] run scoreboard players add @s rpg_dm 1
execute as @a[tag=rpg.dm.job,scores={rpg_dm=5..}] at @s run function rpg:town/demon/job_done
