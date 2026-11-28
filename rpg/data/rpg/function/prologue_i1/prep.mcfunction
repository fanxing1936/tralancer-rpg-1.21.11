# 等强制加载的区块真正载入（实测 2 秒不一定够，木桶会放不下去）：载入了再搭场地，再过 1 秒把人接进来
execute if score #built rpg_pr_i1 matches 0 if score #t rpg_pr_i1 matches 20.. in rpg:armageddon if loaded 32 30 30 if loaded 38 30 32 if loaded -16 80 -16 if loaded 16 80 16 if loaded 40 80 0 if loaded -36 80 0 if loaded 0 40 0 positioned 0 80 0 run function rpg:prologue_i1/arena/build_go
execute if score #built rpg_pr_i1 matches 0 if score #t rpg_pr_i1 matches 600.. run function rpg:prologue_i1/prep_fail
execute if score #built rpg_pr_i1 matches 1 run scoreboard players add #bt rpg_pr_i1 1
execute if score #bt rpg_pr_i1 matches 20 as @a[tag=rpg.pr.join1] run function rpg:prologue_i1/join
execute if score #bt rpg_pr_i1 matches 21 if entity @a[tag=rpg.pri1] run function rpg:prologue_i1/lobby/begin
execute if score #bt rpg_pr_i1 matches 60.. unless entity @a[tag=rpg.pri1] run function rpg:prologue_i1/cleanup
