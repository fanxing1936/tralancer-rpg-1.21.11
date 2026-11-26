# 连招里不抽弓弩：最多重抽三次
function rpg:daath_fight/weapon/pick
execute if score @s rpg_dt_wc matches 8..9 run function rpg:daath_fight/weapon/pick
execute if score @s rpg_dt_wc matches 8..9 run function rpg:daath_fight/weapon/pick
execute if score @s rpg_dt_wc matches 8..9 run function rpg:daath_fight/weapon/pick
execute if score @s rpg_dt_wc matches 8..9 run function rpg:daath_fight/weapon/none
