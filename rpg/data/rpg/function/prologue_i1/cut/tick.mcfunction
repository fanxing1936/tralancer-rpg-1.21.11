# 过场中每刻：按段分派；每 10 刻把镜头重新附一次（旁观者按潜行会脱离附身）
execute if score #cut rpg_pr_i1 matches 1 run function rpg:prologue_i1/cut/s1/tick
execute if score #cut rpg_pr_i1 matches 3 run function rpg:prologue_i1/cut/s3/tick
execute if score #cut rpg_pr_i1 matches 4 run function rpg:prologue_i1/cut/s4/tick
execute if score #cut rpg_pr_i1 matches 6 run function rpg:prologue_i1/cut/s6/tick
execute if score #cut rpg_pr_i1 matches 7 run function rpg:prologue_i1/cut/s7/tick
scoreboard players operation #m rpg_pr_i1 = #ct rpg_pr_i1
scoreboard players operation #m rpg_pr_i1 %= #ten rpg_pr_i1
execute if score #m rpg_pr_i1 matches 0 as @a[tag=rpg.pri1,gamemode=spectator] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1,distance=0..] @s
function rpg:prologue_i1/cut/fx_tick
