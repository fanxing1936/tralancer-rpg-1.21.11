scoreboard players add @s rpg_dt_win 1
function rpg:daath_fight/pl/out
execute unless score @s rpg_daath matches 1 run function rpg:sephira/daath/pass
function rpg:daath_fight/reward
execute if score @s rpg_ps_11 matches 1 if score @s rpg_pa_wn matches 1 run scoreboard players set @s rpg_pa_11 1
