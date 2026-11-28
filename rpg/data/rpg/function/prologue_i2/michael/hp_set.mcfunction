# 血池按人数：400 + 200×人数（1 人 600，4 人 1200）
tag @s add rpg.pr.hpset
scoreboard players operation #mmax rpg_pr_i2 = #n rpg_pr_i2
scoreboard players set #k rpg_pr_i2 200
scoreboard players operation #mmax rpg_pr_i2 *= #k rpg_pr_i2
scoreboard players add #mmax rpg_pr_i2 400
execute store result entity @s Health float 1 run scoreboard players get #mmax rpg_pr_i2
execute store result storage rpg:pr_i2 tmp.hp int 1 run scoreboard players get #mmax rpg_pr_i2
function rpg:prologue_i2/michael/hp_attr with storage rpg:pr_i2 tmp
scoreboard players operation @s rpg_mk_h = #mmax rpg_pr_i2
execute store result bossbar rpg:michael_boss_i2 max run scoreboard players get #mmax rpg_pr_i2
