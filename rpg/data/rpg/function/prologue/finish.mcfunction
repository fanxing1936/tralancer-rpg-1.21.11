# 结尾：送回原处；第一次通关的人得到米迦勒之羽
execute if score #t rpg_pr matches 1 run function rpg:prologue/sub/u14
execute if score #t rpg_pr matches 40 as @a[tag=rpg.pr] run function rpg:prologue/give_back
execute if score #t rpg_pr matches 41 run function rpg:prologue/cleanup
