
# @s 是本次受击实体；四条入口都通过 on attacker 取得唯一技能持有者。
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={sun=0..},tag=rpg.h.sun_tag1] run function rpg:item/legacy_advanced/hit/epic_sun
execute at @s on attacker if entity @s[scores={ice=0..},tag=rpg.h.ice_tag1] run function rpg:item/legacy_advanced/hit/epic_ice
execute at @s on attacker if entity @s[scores={steel=0..},tag=rpg.h.steel_tag1] run function rpg:item/legacy_advanced/hit/epic_steel
execute at @s on attacker if entity @s[scores={sea=0..},tag=rpg.h.sea_tag1] run function rpg:item/legacy_advanced/hit/epic_sea
tag @s remove rpg.legacy.advanced_target
