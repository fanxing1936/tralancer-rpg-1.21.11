execute as @e[tag=rpg.pf.line,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rpg.pf.line,limit=1] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d rpg_pf
execute as @e[tag=rpg.pf.line,limit=1] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d rpg_pf
execute as @e[tag=rpg.pf.line,limit=1] run data merge entity @s {start_interpolation:0}
