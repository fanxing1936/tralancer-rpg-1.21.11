execute store result score #th rpg_fo run data get entity @s Health 10
execute unless score #th rpg_fo > #ph rpg_fo run return 0
scoreboard players add #pct rpg_fo 10
execute if entity @a[tag=rpg.fo.me,limit=1,scores={rpg_sef=5..}] run scoreboard players add #pct rpg_fo 10
