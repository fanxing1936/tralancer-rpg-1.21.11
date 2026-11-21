# 退回槽里原来的符文，再写入新的。
$data modify storage rpg:forge g.o set from entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.runes[$(i)]
execute unless data storage rpg:forge g{o:"none"} run function rpg:forge/op/rune/refund
$data modify entity @e[type=minecraft:item_display,tag=rpg.fg.ws,limit=1] item.components."minecraft:custom_data".rpg_eq.runes[$(i)] set value "$(v)"
