# 判负：不会真的死（as 挑战者）
scoreboard players set @s rpg_dt_ph 5
scoreboard players set @s rpg_dt_pt 0
execute as @e[type=minecraft:vindicator,tag=rpg.dt.it,limit=1] at @s run function rpg:daath_fight/hurt/fail_it
