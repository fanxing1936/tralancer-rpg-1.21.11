# 档位：每段 20 档
scoreboard players operation #s rpg_dt = @s rpg_dt_h
scoreboard players operation #k rpg_dt = @s rpg_dt_mx
scoreboard players set #20 rpg_dt 20
scoreboard players operation #s rpg_dt *= #20 rpg_dt
scoreboard players operation #k rpg_dt *= #10 rpg_dt
scoreboard players operation #j rpg_dt = #k rpg_dt
scoreboard players remove #j rpg_dt 1
scoreboard players operation #s rpg_dt += #j rpg_dt
scoreboard players operation #s rpg_dt /= #k rpg_dt
execute if score #s rpg_dt matches 21.. run scoreboard players set #s rpg_dt 20
execute if score #s rpg_dt matches ..0 run scoreboard players set #s rpg_dt 0
execute if score #s rpg_dt = @s rpg_dt_bar run return 0
scoreboard players operation @s rpg_dt_bar = #s rpg_dt
execute store result storage rpg:daath t.n int 1 run scoreboard players get @s rpg_dt
execute store result storage rpg:daath t.v int 1 run scoreboard players get #s rpg_dt
execute store result storage rpg:daath t.st int 1 run scoreboard players get @s rpg_dt_st
function rpg:daath_fight/bar/m with storage rpg:daath t
