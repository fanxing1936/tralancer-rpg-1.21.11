execute as @a[scores={rpg_pr_lv=1..}] run function rpg:prologue/rejoin
execute unless score #state rpg_pr matches 1.. run return 0
scoreboard players add #t rpg_pr 1
execute if score #state rpg_pr matches 1 run function rpg:prologue/prep
execute if score #state rpg_pr matches 2 run function rpg:prologue/lobby/tick
execute if score #cut rpg_pr matches 1.. run function rpg:prologue/cut/tick
execute if score #state rpg_pr matches 4 run function rpg:prologue/wave/tick
execute if score #state rpg_pr matches 7 run function rpg:prologue/michael/tick
execute if score #state rpg_pr matches 10 run function rpg:prologue/finish
function rpg:prologue/sub/tick
function rpg:prologue/music/tick
# 场地上弹出来的红石粉（群系血迹是红石线，压平/踩碎石台时会掉）每秒清一次
scoreboard players add #sweep rpg_pr 1
execute if score #sweep rpg_pr matches 20.. run function rpg:prologue/arena/sweep
execute as @a[tag=rpg.pr] at @s run function rpg:prologue/player/tick
execute if score #state rpg_pr matches 2.. unless entity @a[tag=rpg.pr] run function rpg:prologue/cleanup
