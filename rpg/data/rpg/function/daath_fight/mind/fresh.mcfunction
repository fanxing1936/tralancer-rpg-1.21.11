# 换招了
scoreboard players set @s rpg_dt_same 0
execute if entity @s[tag=rpg.dt.loop] run function rpg:daath_fight/mind/unloop
