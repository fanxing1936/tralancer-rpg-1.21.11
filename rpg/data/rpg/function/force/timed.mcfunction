# 带时限的效果（as 实体）：到时撤掉
execute if score @s rpg_fo_end > #now rpg_fo run return 0
attribute @s minecraft:armor modifier remove rpg:fo_rot
execute if entity @s[tag=rpg.fo.pup] at @s run particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 20
execute if entity @s[tag=rpg.fo.pup] run tp @s ~ -400 ~
execute if entity @s[tag=rpg.fo.pup] run kill @s
tag @s remove rpg.fo.timed
