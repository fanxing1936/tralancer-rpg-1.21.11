execute unless score #state rpg_pr_i1 matches 1.. run return 0
scoreboard players add #t rpg_pr_i1 1
execute if score #state rpg_pr_i1 matches 1 run function rpg:prologue_i1/prep
execute if score #state rpg_pr_i1 matches 2 run function rpg:prologue_i1/lobby/tick
execute if score #cut rpg_pr_i1 matches 1.. run function rpg:prologue_i1/cut/tick
execute if score #state rpg_pr_i1 matches 4 run function rpg:prologue_i1/wave/tick
execute if score #state rpg_pr_i1 matches 7 run function rpg:prologue_i1/michael/tick
execute if score #state rpg_pr_i1 matches 10 run function rpg:prologue_i1/finish
function rpg:prologue_i1/sub/tick
function rpg:prologue_i1/music/tick
# 场地上弹出来的红石粉（群系血迹是红石线，压平/踩碎石台时会掉）每秒清一次
scoreboard players add #sweep rpg_pr_i1 1
execute if score #sweep rpg_pr_i1 matches 20.. run function rpg:prologue_i1/arena/sweep
execute as @a[tag=rpg.pri1] at @s run function rpg:prologue_i1/player/tick
execute if score #state rpg_pr_i1 matches 2.. unless entity @a[tag=rpg.pri1] run function rpg:prologue_i1/cleanup
