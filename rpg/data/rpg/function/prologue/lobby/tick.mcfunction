# 大厅（每刻）：站上祭坛就选定；人齐倒数 3 秒；满 60 秒没选的自动分配
execute if score #taken1 rpg_pr matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt1] at @s as @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue/lobby/pick_1
execute if score #taken1 rpg_pr matches 1 if score #sub rpg_pr matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt1] at @s if entity @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue/sub/u06
execute if score #taken2 rpg_pr matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt2] at @s as @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue/lobby/pick_2
execute if score #taken2 rpg_pr matches 1 if score #sub rpg_pr matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt2] at @s if entity @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue/sub/u06
execute if score #taken3 rpg_pr matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt3] at @s as @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue/lobby/pick_3
execute if score #taken3 rpg_pr matches 1 if score #sub rpg_pr matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt3] at @s if entity @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue/sub/u06
execute if score #taken4 rpg_pr matches 0 as @e[type=minecraft:marker,tag=rpg.pr.alt4] at @s as @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0},limit=1] run function rpg:prologue/lobby/pick_4
execute if score #taken4 rpg_pr matches 1 if score #sub rpg_pr matches ..0 as @e[type=minecraft:marker,tag=rpg.pr.alt4] at @s if entity @a[tag=rpg.pr,distance=..0.9,scores={rpg_pr_role=0}] run function rpg:prologue/sub/u06
execute store result score #n rpg_pr if entity @a[tag=rpg.pr]
execute store result score #r rpg_pr if entity @a[tag=rpg.pr,scores={rpg_pr_role=1..}]
execute if score #t rpg_pr matches 1200.. run function rpg:prologue/lobby/auto
execute if score #cd rpg_pr matches 0 if score #r rpg_pr = #n rpg_pr run function rpg:prologue/lobby/ready
execute if score #cd rpg_pr matches 1.. run scoreboard players add #cd rpg_pr 1
execute if score #cd rpg_pr matches 61.. run function rpg:prologue/lobby/go
