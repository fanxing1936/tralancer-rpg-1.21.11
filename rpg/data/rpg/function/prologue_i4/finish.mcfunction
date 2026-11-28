# 结尾：送回原处；第一次通关的人得到米迦勒之羽
execute if score #t rpg_pr_i4 matches 1 run function rpg:prologue_i4/sub/u14
execute if score #t rpg_pr_i4 matches 40 as @a[tag=rpg.pri4] run function rpg:prologue_i4/give_back
execute if score #t rpg_pr_i4 matches 41 run function rpg:prologue_i4/cleanup
