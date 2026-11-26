# 抽一道题，三个答案放进 t.a0 t.a1 t.a2（a0 是真的），再打乱
execute store result score #q rpg_dt run random value 0..7
execute if score #q rpg_dt matches 0 run function rpg:daath_fight/ask/q0
execute if score #q rpg_dt matches 1 run function rpg:daath_fight/ask/q1
execute if score #q rpg_dt matches 2 run function rpg:daath_fight/ask/q2
execute if score #q rpg_dt matches 3 run function rpg:daath_fight/ask/q3
execute if score #q rpg_dt matches 4 run function rpg:daath_fight/ask/q4
execute if score #q rpg_dt matches 5 run function rpg:daath_fight/ask/q5
execute if score #q rpg_dt matches 6 run function rpg:daath_fight/ask/q6
execute if score #q rpg_dt matches 7 run function rpg:daath_fight/ask/q7
execute store result score @s rpg_dt_q run random value 0..2
function rpg:daath_fight/ask/show with storage rpg:daath t
