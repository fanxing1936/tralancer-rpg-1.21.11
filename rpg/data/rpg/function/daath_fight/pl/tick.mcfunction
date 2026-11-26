# 挑战者每刻（as/at 玩家）
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
function rpg:daath_fight/pl/check with storage rpg:daath t
execute unless score @s rpg_dt matches 1.. run return 0
execute if score @s rpg_dt_dc matches 1.. run return run function rpg:daath_fight/pl/died
scoreboard players add @s rpg_dt_pt 1
execute if score @s rpg_dt_ph matches 1 run return run function rpg:daath_fight/pl/sink
execute if score @s rpg_dt_ph matches 2 run return run function rpg:daath_fight/pl/arrive
execute if score @s rpg_dt_ph matches 3 run return run function rpg:daath_fight/pl/bound
execute if score @s rpg_dt_ph matches 4 run return run function rpg:daath_fight/pl/rise
execute if score @s rpg_dt_ph matches 5 run return run function rpg:daath_fight/pl/lost
