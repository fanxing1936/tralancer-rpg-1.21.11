function rpg:daath_fight/sk/end
function rpg:daath/anim/enter/idle
execute if score @s rpg_dt_st matches 1 run scoreboard players set @s rpg_dt_gap 20
execute if score @s rpg_dt_st matches 2 run scoreboard players set @s rpg_dt_gap 13
