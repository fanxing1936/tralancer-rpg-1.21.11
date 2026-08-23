# 刚到场那几刻反复补画。
#
# 装备带来的属性修饰符不是在 summon 那一刻就位的 —— 实测刚生出来读 armor
# 得到的是没算装备的基数。到底几刻才稳没有保证，所以干脆连画 6 刻再收手：
# 这段开销只在有人刚到场时存在，平时那道存在性判定直接落空。
execute as @e[type=minecraft:husk,tag=rpg.sq.fresh] run function rpg:squad/board
execute as @e[type=minecraft:husk,tag=rpg.sq.fresh] run scoreboard players add @s rpg_sq_fr 1
tag @e[type=minecraft:husk,tag=rpg.sq.fresh,scores={rpg_sq_fr=6..}] remove rpg.sq.fresh
