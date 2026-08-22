# 三件新武器的每刻入口。每条都先过握持判定 ——
# 没人拿着时整段跳过，空闲一刻只剩三次标签检查。
execute if entity @a[tag=rpg.h.dawn_tag1] run function rpg:item/epic/saw
execute if entity @a[tag=rpg.h.chime_tag1] run function rpg:item/epic/chime
execute if entity @a[tag=rpg.h.forge_tag1] run function rpg:item/epic/forge
