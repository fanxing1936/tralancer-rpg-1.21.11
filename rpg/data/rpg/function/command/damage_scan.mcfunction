# Snapshot health for entities a player could plausibly have hit, and flag the
# ones whose health moved since last tick.  Run once per player from
# rpg:command/index instead of once per weapon-effect line for every entity.
execute as @e[type=!#rpg:no_damage_track,distance=..64] store result score @s damage_action run data get entity @s Health
# 第一次见到的实体先把基准对齐：否则它会被当成"刚受伤"，
# 读档时区块一批批加载，每批新实体都会误触发一次全部武器判定 —— 就是进档后那阵卡顿。
# `unless score X = X` 在分数不存在时成立，是判断"这个分数有没有值"的惯用写法。
execute as @e[type=!#rpg:no_damage_track,distance=..64] unless score @s damage_timing = @s damage_timing run scoreboard players operation @s damage_timing = @s damage_action
execute as @e[type=!#rpg:no_damage_track,distance=..64] unless score @s damage_action = @s damage_timing run tag @s add rpg.hurt
