# 朗基努斯的普通命中刻下王座印，供主动技精确处决。
scoreboard players set @e[tag=rpg.legacy.target,limit=1] rpg_throne_mark 120
scoreboard players operation @e[tag=rpg.legacy.target,limit=1] rpg_throne_owner = @s rpg_legacy_uid
tag @e[tag=rpg.legacy.target,limit=1] add rpg.throne.mark
execute at @e[tag=rpg.legacy.target,limit=1] run particle minecraft:dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:1.4} ~ ~1 ~ 0.25 0.45 0.25 0.03 10 force
