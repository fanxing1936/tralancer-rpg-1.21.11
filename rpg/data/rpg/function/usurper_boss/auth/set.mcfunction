tp @s ~ ~ ~ ~ ~
data merge entity @s {start_interpolation:0,interpolation_duration:2}
execute store result entity @s transformation.scale[2] float 1 run scoreboard players get #d rpg_ub
execute store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d rpg_ub
