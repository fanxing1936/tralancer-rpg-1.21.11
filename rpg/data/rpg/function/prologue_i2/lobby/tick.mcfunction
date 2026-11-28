# 大厅（每刻）：站上祭坛就选定；人齐倒数 3 秒；满 60 秒没选的自动分配
execute if score #taken1 rpg_pr_i2 matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt1,distance=0..] at @s as @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_1
execute if score #taken1 rpg_pr_i2 matches 1 if score #sub rpg_pr_i2 matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt1,distance=0..] at @s if entity @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue_i2/sub/u06
execute if score #taken2 rpg_pr_i2 matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt2,distance=0..] at @s as @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_2
execute if score #taken2 rpg_pr_i2 matches 1 if score #sub rpg_pr_i2 matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt2,distance=0..] at @s if entity @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue_i2/sub/u06
execute if score #taken3 rpg_pr_i2 matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt3,distance=0..] at @s as @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_3
execute if score #taken3 rpg_pr_i2 matches 1 if score #sub rpg_pr_i2 matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt3,distance=0..] at @s if entity @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue_i2/sub/u06
execute if score #taken4 rpg_pr_i2 matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt4,distance=0..] at @s as @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue_i2/lobby/pick_4
execute if score #taken4 rpg_pr_i2 matches 1 if score #sub rpg_pr_i2 matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt4,distance=0..] at @s if entity @a[tag=rpg.pri2,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue_i2/sub/u06
execute store result score #n rpg_pr_i2 if entity @a[tag=rpg.pri2]
execute store result score #r rpg_pr_i2 if entity @a[tag=rpg.pri2,scores={rpg_pr_role=1..}]
execute if score #t rpg_pr_i2 matches 1200.. run function rpg:prologue_i2/lobby/auto
execute if score #cd rpg_pr_i2 matches 0 if score #r rpg_pr_i2 = #n rpg_pr_i2 run function rpg:prologue_i2/lobby/ready
execute if score #cd rpg_pr_i2 matches 1.. run scoreboard players add #cd rpg_pr_i2 1
execute if score #cd rpg_pr_i2 matches 61.. run function rpg:prologue_i2/lobby/go
