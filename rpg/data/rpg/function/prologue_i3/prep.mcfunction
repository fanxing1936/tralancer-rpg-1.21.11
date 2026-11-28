# 等强制加载的区块真正载入（实测 2 秒不一定够，木桶会放不下去）：载入了再搭场地，再过 1 秒把人接进来
execute if score #built rpg_pr_i3 matches 0 if score #t rpg_pr_i3 matches 20.. in rpg:armageddon_3 if loaded 32 30 30 if loaded 38 30 32 if loaded -16 80 -16 if loaded 16 80 16 if loaded 40 80 0 if loaded -36 80 0 if loaded 0 40 0 positioned 0 80 0 run function rpg:prologue_i3/arena/build_go
execute if score #built rpg_pr_i3 matches 0 if score #t rpg_pr_i3 matches 600.. run function rpg:prologue_i3/prep_fail
execute if score #built rpg_pr_i3 matches 1 run scoreboard players add #bt rpg_pr_i3 1
execute if score #bt rpg_pr_i3 matches 20 as @a[tag=rpg.pr.join3] run function rpg:prologue_i3/join
execute if score #bt rpg_pr_i3 matches 21 if entity @a[tag=rpg.pri3] run function rpg:prologue_i3/lobby/begin
execute if score #bt rpg_pr_i3 matches 60.. unless entity @a[tag=rpg.pri3] run function rpg:prologue_i3/cleanup
