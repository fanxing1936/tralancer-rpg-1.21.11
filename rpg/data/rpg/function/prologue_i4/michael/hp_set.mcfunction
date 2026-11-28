# 血池按人数：400 + 200×人数（1 人 600，4 人 1200）
tag @s add rpg.pr.hpset
scoreboard players operation #mmax rpg_pr_i4 = #n rpg_pr_i4
scoreboard players set #k rpg_pr_i4 200
scoreboard players operation #mmax rpg_pr_i4 *= #k rpg_pr_i4
scoreboard players add #mmax rpg_pr_i4 400
execute store result entity @s Health float 1 run scoreboard players get #mmax rpg_pr_i4
execute store result storage rpg:pr_i4 tmp.hp int 1 run scoreboard players get #mmax rpg_pr_i4
function rpg:prologue_i4/michael/hp_attr with storage rpg:pr_i4 tmp
scoreboard players operation @s rpg_mk_h = #mmax rpg_pr_i4
execute store result bossbar rpg:michael_boss_i4 max run scoreboard players get #mmax rpg_pr_i4
