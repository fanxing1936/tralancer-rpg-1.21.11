# 选好火点却没开炉，1 分钟后作废。
scoreboard players add @s rpg_fg_t 1
execute if score @s rpg_fg_t matches 1200.. run kill @s
