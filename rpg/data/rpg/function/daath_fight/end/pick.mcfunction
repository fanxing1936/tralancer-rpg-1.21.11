kill @e[type=minecraft:interaction,tag=rpg.dt.touch,distance=..6]
scoreboard players set @s rpg_dt_t 0
execute unless score @a[tag=rpg.dt.me,limit=1] rpg_dt_die matches 1.. run scoreboard players operation @a[tag=rpg.dt.me,limit=1] rpg_dt_die = @s rpg_dt_q
