
# 无垠星空：受击者 -> 本次攻击者。随机数和全部增益都属于该攻击者。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={saber=0..},tag=rpg.h.saber_tag1] run function rpg:item/legacy_advanced/hit/saber
tag @s remove rpg.legacy.advanced_target
