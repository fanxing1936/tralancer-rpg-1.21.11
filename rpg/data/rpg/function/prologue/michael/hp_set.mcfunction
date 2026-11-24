# 血池按人数：400 + 200×人数（1 人 600，4 人 1200）
tag @s add rpg.pr.hpset
scoreboard players operation #mmax rpg_pr = #n rpg_pr
scoreboard players set #k rpg_pr 200
scoreboard players operation #mmax rpg_pr *= #k rpg_pr
scoreboard players add #mmax rpg_pr 400
execute store result entity @s Health float 1 run scoreboard players get #mmax rpg_pr
execute store result storage rpg:pr tmp.hp int 1 run scoreboard players get #mmax rpg_pr
function rpg:prologue/michael/hp_attr with storage rpg:pr tmp
scoreboard players operation @s rpg_mk_h = #mmax rpg_pr
execute store result bossbar rpg:michael_boss max run scoreboard players get #mmax rpg_pr
