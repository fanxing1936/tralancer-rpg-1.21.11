# 场次对不上（掉线太久、服务器清过）：送回去
$execute if score #b$(n) rpg_dt matches 1 if score #sid$(n) rpg_dt = @s rpg_dt_sid run return 0
function rpg:daath_fight/pl/out
