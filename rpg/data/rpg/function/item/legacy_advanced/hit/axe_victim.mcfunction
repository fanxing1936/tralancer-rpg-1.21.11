
# 教条战斧：纹饰由攻击者主手判定，效果只落在本次受击者或攻击者本人。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={axe=0..},tag=rpg.h.axe_tag1] run function rpg:item/legacy_advanced/hit/axe
tag @s remove rpg.legacy.advanced_target
