# 路西法必须有人选：没人选时，编号最小的那位改成路西法（他原来的位子空出来）
execute if score #taken1 rpg_pr_i1 matches 1 run return 0
execute as @a[tag=rpg.pri1,scores={rpg_pr_id=1}] run function rpg:prologue_i1/lobby/to_lucifer
execute if score #taken1 rpg_pr_i1 matches 0 as @a[tag=rpg.pri1,scores={rpg_pr_id=2}] run function rpg:prologue_i1/lobby/to_lucifer
execute if score #taken1 rpg_pr_i1 matches 0 as @a[tag=rpg.pri1,scores={rpg_pr_id=3}] run function rpg:prologue_i1/lobby/to_lucifer
execute if score #taken1 rpg_pr_i1 matches 0 as @a[tag=rpg.pri1,scores={rpg_pr_id=4}] run function rpg:prologue_i1/lobby/to_lucifer
