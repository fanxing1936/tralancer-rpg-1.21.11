
# 如意金箍棒：每个攻击者独立掷签，不读取或清空别人的 random。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={wukong=0..},tag=rpg.h.wukong_tag1] run function rpg:item/legacy_advanced/hit/wukong
tag @s remove rpg.legacy.advanced_target
