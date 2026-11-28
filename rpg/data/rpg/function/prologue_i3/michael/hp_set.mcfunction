# 血池按人数：400 + 200×人数（1 人 600，4 人 1200）
tag @s add rpg.pr.hpset
scoreboard players operation #mmax rpg_pr_i3 = #n rpg_pr_i3
scoreboard players set #k rpg_pr_i3 200
scoreboard players operation #mmax rpg_pr_i3 *= #k rpg_pr_i3
scoreboard players add #mmax rpg_pr_i3 400
execute store result entity @s Health float 1 run scoreboard players get #mmax rpg_pr_i3
execute store result storage rpg:pr_i3 tmp.hp int 1 run scoreboard players get #mmax rpg_pr_i3
function rpg:prologue_i3/michael/hp_attr with storage rpg:pr_i3 tmp
scoreboard players operation @s rpg_mk_h = #mmax rpg_pr_i3
execute store result bossbar rpg:michael_boss_i3 max run scoreboard players get #mmax rpg_pr_i3
