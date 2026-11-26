# 抽一把武器拿在手里，#c 类别记进 rpg_dt_wc（as 影子）
execute if score @s rpg_dt_sw matches 1.. run return run function rpg:daath_fight/weapon/stolen
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
function rpg:daath_fight/weapon/len with storage rpg:daath t
execute if score #len rpg_dt matches ..0 run return run function rpg:daath_fight/weapon/none
scoreboard players remove #len rpg_dt 1
execute store result storage rpg:daath t.max int 1 run scoreboard players get #len rpg_dt
function rpg:daath_fight/weapon/roll with storage rpg:daath t
function rpg:daath_fight/weapon/take with storage rpg:daath t
function rpg:daath_fight/weapon/hold
