# 没人拿着圣骸、场上也没有未熄的圣焰时整段跳过。
execute if entity @a[tag=rpg.h.michael_rib_tag1] run return run function rpg:item/extra/michael
execute if entity @a[tag=rpg.o.michael_rib_tag1] run return run function rpg:item/extra/michael
execute if entity @a[tag=rpg.h.michael_spine_tag1] run return run function rpg:item/extra/michael
execute if entity @a[tag=rpg.o.michael_spine_tag1] run return run function rpg:item/extra/michael
execute if score #mi_live rpg_mi_tmp matches 1.. run function rpg:item/extra/michael
