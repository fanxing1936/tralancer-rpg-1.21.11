execute if entity @s[tag=rpg.dt.mute] run return 0
scoreboard players remove @s rpg_dt_bgm 1
execute if score @s rpg_dt_bgm matches 1.. run return 0
execute if score @s rpg_dt_st matches 1 run function rpg:daath_fight/music/1
execute if score @s rpg_dt_st matches 2 run function rpg:daath_fight/music/2
