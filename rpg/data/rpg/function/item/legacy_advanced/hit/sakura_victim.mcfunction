
tag @e[tag=rpg.legacy.advanced_target] remove rpg.legacy.advanced_target
tag @s add rpg.legacy.advanced_target
execute at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.sakura_tag1] run function rpg:item/legacy_advanced/hit/sakura
execute at @s on attacker if entity @s[scores={sakura=0..},tag=rpg.h.night_tag1] run function rpg:item/legacy_advanced/hit/night
tag @s remove rpg.legacy.advanced_target
