# 过场中每刻：按段分派；每 10 刻把镜头重新附一次（旁观者按潜行会脱离附身）
execute if score #cut rpg_pr matches 1 run function rpg:prologue/cut/s1/tick
execute if score #cut rpg_pr matches 3 run function rpg:prologue/cut/s3/tick
execute if score #cut rpg_pr matches 4 run function rpg:prologue/cut/s4/tick
execute if score #cut rpg_pr matches 6 run function rpg:prologue/cut/s6/tick
execute if score #cut rpg_pr matches 7 run function rpg:prologue/cut/s7/tick
scoreboard players operation #m rpg_pr = #ct rpg_pr
scoreboard players operation #m rpg_pr %= #ten rpg_pr
execute if score #m rpg_pr matches 0 as @a[tag=rpg.pr,gamemode=spectator] run spectate @e[type=minecraft:item_display,tag=rpg.pr.cam,limit=1] @s
function rpg:prologue/cut/fx_tick
