# 裂甲［被动］—— 破开护甲：虚弱削弱其输出，发光让它无处可藏。
execute if entity @e[tag=rpg.hurt] run function rpg:item/rune/sunder/g0
tag @a[tag=rpg.rune.sunder] remove rpg.rune.sunder
