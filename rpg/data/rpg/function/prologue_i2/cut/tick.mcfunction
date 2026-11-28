# 过场中每刻：按段分派；每 10 刻把镜头重新附一次（旁观者按潜行会脱离附身）
execute if score #cut rpg_pr_i2 matches 1 run function rpg:prologue_i2/cut/s1/tick
execute if score #cut rpg_pr_i2 matches 3 run function rpg:prologue_i2/cut/s3/tick
execute if score #cut rpg_pr_i2 matches 4 run function rpg:prologue_i2/cut/s4/tick
execute if score #cut rpg_pr_i2 matches 6 run function rpg:prologue_i2/cut/s6/tick
execute if score #cut rpg_pr_i2 matches 7 run function rpg:prologue_i2/cut/s7/tick
scoreboard players operation #m rpg_pr_i2 = #ct rpg_pr_i2
scoreboard players operation #m rpg_pr_i2 %= #ten rpg_pr_i2
execute if score #m rpg_pr_i2 matches 0 as @a[tag=rpg.pri2,gamemode=spectator] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] @s
function rpg:prologue_i2/cut/fx_tick
