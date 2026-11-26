# 夺来的那把：之后只用它
execute store result storage rpg:daath t.id int 1 run scoreboard players get @a[tag=rpg.dt.me,limit=1] rpg_fg_id
function rpg:daath_fight/weapon/stolen_m with storage rpg:daath t
function rpg:daath_fight/weapon/hold
