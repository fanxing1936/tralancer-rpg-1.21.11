# 满 60 秒：没选的人按 路西法 → 别西卜 → 贝利尔 → 玛门 的顺序补上空位
execute if score #taken1 rpg_pr_i2 matches 0 as @a[tag=rpg.pri2,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_1
execute if score #taken2 rpg_pr_i2 matches 0 as @a[tag=rpg.pri2,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_2
execute if score #taken3 rpg_pr_i2 matches 0 as @a[tag=rpg.pri2,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_3
execute if score #taken4 rpg_pr_i2 matches 0 as @a[tag=rpg.pri2,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_4
