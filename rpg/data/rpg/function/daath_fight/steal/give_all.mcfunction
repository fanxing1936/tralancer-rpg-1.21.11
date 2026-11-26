# 全部归还（as 玩家）
execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id
function rpg:daath_fight/steal/give_w with storage rpg:daath t
function rpg:daath_fight/steal/give_a with storage rpg:daath t
function rpg:daath_fight/steal/done with storage rpg:daath t
