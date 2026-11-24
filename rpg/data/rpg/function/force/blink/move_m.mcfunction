tp @a[tag=rpg.fo.me,limit=1] ~ ~ ~
particle minecraft:large_smoke ~ ~1 ~ 0.15 0.3 0.15 0 2
scoreboard players remove #r rpg_fo 1
execute if score #r rpg_fo matches 1.. run function rpg:force/blink/step_m
