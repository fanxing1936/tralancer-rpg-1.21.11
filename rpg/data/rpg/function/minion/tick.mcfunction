# 35 种罪仆共用十刻节拍，场上无罪仆时不会进入本系统。
scoreboard players add #clock rpg_mn_tick 1
execute if score #clock rpg_mn_tick matches 10.. run function rpg:minion/beat
