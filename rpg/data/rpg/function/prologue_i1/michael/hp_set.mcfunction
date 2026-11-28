# 血池按人数：400 + 200×人数（1 人 600，4 人 1200）
tag @s add rpg.pr.hpset
scoreboard players operation #mmax rpg_pr_i1 = #n rpg_pr_i1
scoreboard players set #k rpg_pr_i1 200
scoreboard players operation #mmax rpg_pr_i1 *= #k rpg_pr_i1
scoreboard players add #mmax rpg_pr_i1 400
execute store result entity @s Health float 1 run scoreboard players get #mmax rpg_pr_i1
execute store result storage rpg:pr_i1 tmp.hp int 1 run scoreboard players get #mmax rpg_pr_i1
function rpg:prologue_i1/michael/hp_attr with storage rpg:pr_i1 tmp
scoreboard players operation @s rpg_mk_h = #mmax rpg_pr_i1
execute store result bossbar rpg:michael_boss_i1 max run scoreboard players get #mmax rpg_pr_i1
