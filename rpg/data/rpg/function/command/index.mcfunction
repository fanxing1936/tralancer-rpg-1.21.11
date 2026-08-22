# Auto-generated per-tick flag index.
# 每个族群只遍历一次：清标记与判定都在 @s 上完成，
# 于是玩家表每刻只走一遍、掉落物表也只走一遍。

execute as @a run function rpg:command/index_player
execute as @e[type=minecraft:item] run function rpg:command/index_item

## damage detection
tag @e[tag=rpg.hurt] remove rpg.hurt
execute as @a at @s run function rpg:command/damage_scan

tag @a remove rpg.h.jachin_tag1
tag @a remove rpg.h.boaz_tag1
tag @a remove rpg.h.lucifer_tag1
tag @a remove rpg.h.leviathan_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{deep_seek_tag:1b}] run tag @s add rpg.h.deep_seek_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{mischief_tag:1b}] run tag @s add rpg.h.mischief_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{rift_tag:1b}] run tag @s add rpg.h.rift_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{vine_tag:1b}] run tag @s add rpg.h.vine_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{truth_tag:1b}] run tag @s add rpg.h.truth_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{jachin_tag:1b}] run tag @s add rpg.h.jachin_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{boaz_tag:1b}] run tag @s add rpg.h.boaz_tag1
execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{lucifer_tag:1b}] run tag @s add rpg.h.lucifer_tag1

execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{leviathan_tag:1b}] run tag @s add rpg.h.leviathan_tag1

## off-hand item flags
tag @a remove rpg.o.jachin_tag1
tag @a remove rpg.o.boaz_tag1
execute as @a if items entity @s weapon.offhand *[minecraft:custom_data~{jachin_tag:1b}] run tag @s add rpg.o.jachin_tag1
execute as @a if items entity @s weapon.offhand *[minecraft:custom_data~{boaz_tag:1b}] run tag @s add rpg.o.boaz_tag1
