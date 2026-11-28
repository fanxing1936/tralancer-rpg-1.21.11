# 还原一名玩家（as 玩家）
execute store result storage rpg:pr_i3 tmp.id int 1 run scoreboard players get @s rpg_pr_id
execute unless data storage rpg:pr_i3 r.p1 unless data storage rpg:pr_i3 r.p2 unless data storage rpg:pr_i3 r.p3 unless data storage rpg:pr_i3 r.p4 run return run tellraw @s {"text":"[序章] 找不到你的回程记录","color":"red"}
scoreboard players remove #owe rpg_pr_i3 1
scoreboard players reset @s rpg_pr_g
clear @s
execute if score @s rpg_pr_id matches 1 run function rpg:prologue_i3/iso/unstash_1
execute if score @s rpg_pr_id matches 2 run function rpg:prologue_i3/iso/unstash_2
execute if score @s rpg_pr_id matches 3 run function rpg:prologue_i3/iso/unstash_3
execute if score @s rpg_pr_id matches 4 run function rpg:prologue_i3/iso/unstash_4
function rpg:prologue_i3/iso/restore_m with storage rpg:pr_i3 tmp
attribute @s minecraft:max_health modifier remove rpg:prologue/hp
function rpg:prologue_i3/role/avatar_off
stopsound @s record
tag @s remove rpg.pr
tag @s remove rpg.pri3
tag @s remove rpg.pr.mh
scoreboard players reset @s rpg_pr_role
scoreboard players reset @s rpg_pr_id
title @s reset
# 新手开局：序章之后进黑屏欢迎页（add_onboard.py）
execute if entity @s[tag=rpg.ob] run function rpg:onboard/pro/after
