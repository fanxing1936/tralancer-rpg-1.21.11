# @a 的全部 custom_data 标记，逐个实体一次算完。

tag @s remove rpg.h.ashes_tag1
tag @s remove rpg.h.axe_tag1
tag @s remove rpg.h.blil_tag1
tag @s remove rpg.h.blow_tag1
tag @s remove rpg.h.bow_tag1
tag @s remove rpg.h.bubble_tag1
tag @s remove rpg.h.burn_tag1
tag @s remove rpg.h.chainsaw_tag1
tag @s remove rpg.h.chestplate_tag1
tag @s remove rpg.h.damage_tag1
tag @s remove rpg.h.dark_tag1
tag @s remove rpg.h.deep_tag1
tag @s remove rpg.h.devil_tag1
tag @s remove rpg.h.devil_weapon_tag1
tag @s remove rpg.h.devil_weapon_tag2
tag @s remove rpg.h.devil_weapon_tag3
tag @s remove rpg.h.holy_weapon_tag1
tag @s remove rpg.h.holy_weapon_tag2
tag @s remove rpg.h.holy_weapon_tag3
tag @s remove rpg.h.hunter_tag1
tag @s remove rpg.h.ice_tag1
tag @s remove rpg.h.ink_tag1
tag @s remove rpg.h.montain_tag1
tag @s remove rpg.h.night_tag1
tag @s remove rpg.h.pen_tag1
tag @s remove rpg.h.player_tag1
tag @s remove rpg.h.potion_tag1
tag @s remove rpg.h.power_tag1
tag @s remove rpg.h.projectiles_tag1
tag @s remove rpg.h.saber_tag1
tag @s remove rpg.h.sakura_tag1
tag @s remove rpg.h.sea_tag1
tag @s remove rpg.h.skull_tag1
tag @s remove rpg.h.soul_tag1
tag @s remove rpg.h.steel_tag1
tag @s remove rpg.h.sun_tag1
tag @s remove rpg.h.sword_tag1
tag @s remove rpg.h.typhoon_tag1
tag @s remove rpg.h.weapon_tag1
tag @s remove rpg.h.wukong_tag1
tag @s remove rpg.h.deep_seek_tag1
tag @s remove rpg.h.mischief_tag1
tag @s remove rpg.h.rift_tag1
tag @s remove rpg.h.vine_tag1
tag @s remove rpg.h.truth_tag1
tag @s remove rpg.h.jachin_tag1
tag @s remove rpg.h.boaz_tag1
tag @s remove rpg.h.lucifer_tag1
tag @s remove rpg.h.leviathan_tag1
tag @s remove rpg.h.wilt_tag1
tag @s remove rpg.h.sunder_tag1
tag @s remove rpg.h.ebb_tag1
tag @s remove rpg.h.pin_tag1
tag @s remove rpg.h.tide_tag1
tag @s remove rpg.h.quake_tag1
tag @s remove rpg.h.shade_tag1
tag @s remove rpg.o.jachin_tag1
tag @s remove rpg.o.boaz_tag1
tag @s remove rpg.e.chest_absorption_tag1
tag @s remove rpg.e.chest_boom_tag1
tag @s remove rpg.e.chest_chestplate_tag1
tag @s remove rpg.e.chest_health_tag1
tag @s remove rpg.e.chest_weapon_tag1
tag @s remove rpg.e.feet_chestplate_tag1
tag @s remove rpg.e.feet_weapon_tag1
tag @s remove rpg.e.head_chestplate_tag1
tag @s remove rpg.e.head_weapon_tag1
tag @s remove rpg.e.legs_chestplate_tag1
tag @s remove rpg.e.legs_weapon_tag1
tag @s remove rpg.e.offhand_power_tag1
tag @s remove rpg.e.offhand_sakura_tag1

execute if items entity @s weapon.mainhand *[minecraft:custom_data~{ashes_tag:1b}] run tag @s add rpg.h.ashes_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{axe_tag:1b}] run tag @s add rpg.h.axe_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{blil_tag:1b}] run tag @s add rpg.h.blil_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{blow_tag:1b}] run tag @s add rpg.h.blow_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bow_tag:1b}] run tag @s add rpg.h.bow_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bubble_tag:1b}] run tag @s add rpg.h.bubble_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{burn_tag:1b}] run tag @s add rpg.h.burn_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{chainsaw_tag:1b}] run tag @s add rpg.h.chainsaw_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{chestplate_tag:1b}] run tag @s add rpg.h.chestplate_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{damage_tag:1b}] run tag @s add rpg.h.damage_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{dark_tag:1b}] run tag @s add rpg.h.dark_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{deep_tag:1b}] run tag @s add rpg.h.deep_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{devil_tag:1b}] run tag @s add rpg.h.devil_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{devil_weapon_tag:1b}] run tag @s add rpg.h.devil_weapon_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{devil_weapon_tag:2b}] run tag @s add rpg.h.devil_weapon_tag2
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{devil_weapon_tag:3b}] run tag @s add rpg.h.devil_weapon_tag3
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{holy_weapon_tag:1b}] run tag @s add rpg.h.holy_weapon_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{holy_weapon_tag:2b}] run tag @s add rpg.h.holy_weapon_tag2
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{holy_weapon_tag:3b}] run tag @s add rpg.h.holy_weapon_tag3
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{hunter_tag:1b}] run tag @s add rpg.h.hunter_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{ice_tag:1b}] run tag @s add rpg.h.ice_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{ink_tag:1b}] run tag @s add rpg.h.ink_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{montain_tag:1b}] run tag @s add rpg.h.montain_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{night_tag:1b}] run tag @s add rpg.h.night_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pen_tag:1b}] run tag @s add rpg.h.pen_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{player_tag:1b}] run tag @s add rpg.h.player_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{potion_tag:1b}] run tag @s add rpg.h.potion_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{power_tag:1b}] run tag @s add rpg.h.power_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{projectiles_tag:1b}] run tag @s add rpg.h.projectiles_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{saber_tag:1b}] run tag @s add rpg.h.saber_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{sakura_tag:1b}] run tag @s add rpg.h.sakura_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{sea_tag:1b}] run tag @s add rpg.h.sea_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{skull_tag:1b}] run tag @s add rpg.h.skull_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{soul_tag:1b}] run tag @s add rpg.h.soul_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{steel_tag:1b}] run tag @s add rpg.h.steel_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{sun_tag:1b}] run tag @s add rpg.h.sun_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{sword_tag:1b}] run tag @s add rpg.h.sword_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{typhoon_tag:1b}] run tag @s add rpg.h.typhoon_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{weapon_tag:1b}] run tag @s add rpg.h.weapon_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{wukong_tag:1b}] run tag @s add rpg.h.wukong_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{deep_seek_tag:1b}] run tag @s add rpg.h.deep_seek_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{mischief_tag:1b}] run tag @s add rpg.h.mischief_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rift_tag:1b}] run tag @s add rpg.h.rift_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{vine_tag:1b}] run tag @s add rpg.h.vine_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{truth_tag:1b}] run tag @s add rpg.h.truth_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{jachin_tag:1b}] run tag @s add rpg.h.jachin_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{boaz_tag:1b}] run tag @s add rpg.h.boaz_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{lucifer_tag:1b}] run tag @s add rpg.h.lucifer_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{leviathan_tag:1b}] run tag @s add rpg.h.leviathan_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{wilt_tag:1b}] run tag @s add rpg.h.wilt_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{sunder_tag:1b}] run tag @s add rpg.h.sunder_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{ebb_tag:1b}] run tag @s add rpg.h.ebb_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{pin_tag:1b}] run tag @s add rpg.h.pin_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{tide_tag:1b}] run tag @s add rpg.h.tide_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{quake_tag:1b}] run tag @s add rpg.h.quake_tag1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{shade_tag:1b}] run tag @s add rpg.h.shade_tag1
execute if items entity @s weapon.offhand *[minecraft:custom_data~{jachin_tag:1b}] run tag @s add rpg.o.jachin_tag1
execute if items entity @s weapon.offhand *[minecraft:custom_data~{boaz_tag:1b}] run tag @s add rpg.o.boaz_tag1
execute if items entity @s armor.chest *[minecraft:custom_data~{absorption_tag:1b}] run tag @s add rpg.e.chest_absorption_tag1
execute if items entity @s armor.chest *[minecraft:custom_data~{boom_tag:1b}] run tag @s add rpg.e.chest_boom_tag1
execute if items entity @s armor.chest *[minecraft:custom_data~{chestplate_tag:1b}] run tag @s add rpg.e.chest_chestplate_tag1
execute if items entity @s armor.chest *[minecraft:custom_data~{health_tag:1b}] run tag @s add rpg.e.chest_health_tag1
execute if items entity @s armor.chest *[minecraft:custom_data~{weapon_tag:1b}] run tag @s add rpg.e.chest_weapon_tag1
execute if items entity @s armor.feet *[minecraft:custom_data~{chestplate_tag:1b}] run tag @s add rpg.e.feet_chestplate_tag1
execute if items entity @s armor.feet *[minecraft:custom_data~{weapon_tag:1b}] run tag @s add rpg.e.feet_weapon_tag1
execute if items entity @s armor.head *[minecraft:custom_data~{chestplate_tag:1b}] run tag @s add rpg.e.head_chestplate_tag1
execute if items entity @s armor.head *[minecraft:custom_data~{weapon_tag:1b}] run tag @s add rpg.e.head_weapon_tag1
execute if items entity @s armor.legs *[minecraft:custom_data~{chestplate_tag:1b}] run tag @s add rpg.e.legs_chestplate_tag1
execute if items entity @s armor.legs *[minecraft:custom_data~{weapon_tag:1b}] run tag @s add rpg.e.legs_weapon_tag1
execute if items entity @s weapon.offhand *[minecraft:custom_data~{power_tag:1b}] run tag @s add rpg.e.offhand_power_tag1
execute if items entity @s weapon.offhand *[minecraft:custom_data~{sakura_tag:1b}] run tag @s add rpg.e.offhand_sakura_tag1
