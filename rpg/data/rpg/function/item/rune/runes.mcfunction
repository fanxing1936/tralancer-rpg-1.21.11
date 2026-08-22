# 镶嵌符文与符石的每刻入口。每条都先过握持判定 ——
# 没人带着这枚刻印时整段跳过。

execute if entity @a[tag=rpg.h.wilt_tag1] run function rpg:item/rune/wilt
execute if entity @a[tag=rpg.h.sunder_tag1] run function rpg:item/rune/sunder
execute if entity @a[tag=rpg.h.ebb_tag1] run function rpg:item/rune/ebb
execute if entity @a[tag=rpg.h.pin_tag1] run function rpg:item/rune/pin
execute unless entity @a[tag=rpg.h.pin_tag1] if entity @e[type=minecraft:arrow,tag=rpg.rune.pin] run function rpg:item/rune/pin
execute if entity @a[tag=rpg.h.tide_tag1] run function rpg:item/rune/tide
execute if entity @a[tag=rpg.h.quake_tag1] run function rpg:item/rune/quake
execute if entity @a[tag=rpg.h.shade_tag1] run function rpg:item/rune/shade
