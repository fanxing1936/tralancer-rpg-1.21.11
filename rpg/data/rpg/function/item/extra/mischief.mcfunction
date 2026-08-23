# 稚弩［顽劣］
# 不加伤害：命中的目标被恶作剧缠上——眩晕、脱力，并在一段时间内无处可藏。
execute as @e[type=minecraft:arrow,tag=!rpg.mis] on origin if entity @s[tag=rpg.h.mischief_tag1] at @s run tag @e[type=minecraft:arrow,distance=0..2] add rpg.mis
execute if entity @e[tag=rpg.mis] run function rpg:item/extra/mischief/g0
