# 一个实体的份。原本这三行各自开一次 @e[type=!#rpg:no_damage_track,distance=..64]，
# 而那是否定类型过滤 —— 用不上类型索引，三行就是三次真正的全表走查，
# 再乘以在线人数。依赖全在同一个实体身上，所以把循环翻过来结果逐字相同。
execute store result score @s damage_action run data get entity @s Health
# 第一次见到的实体先把基准对齐：否则它会被当成"刚受伤"，
# 读档时区块一批批加载，每批新实体都会误触发一次全部武器判定。
# `unless score X = X` 在分数不存在时成立，是判断"这个分数有没有值"的惯用写法。
execute unless score @s damage_timing = @s damage_timing run scoreboard players operation @s damage_timing = @s damage_action
execute unless score @s damage_action = @s damage_timing run tag @s add rpg.hurt
