# 米迦勒圣骸的每刻结算。由 rpg:item/extra/michael_guard 守卫调用。

# 骨中之骨：一手脊骨、一手肋骨，左右不论
tag @a remove rpg.mi.pair
tag @a[tag=rpg.h.michael_spine_tag1,tag=rpg.o.michael_rib_tag1] add rpg.mi.pair
tag @a[tag=rpg.h.michael_rib_tag1,tag=rpg.o.michael_spine_tag1] add rpg.mi.pair

# 圣焰：握着肋骨（主手或副手）且这一刻打出了伤害
tag @a[tag=rpg.h.michael_rib_tag1,scores={rpg_mi_dmg=1..}] add rpg.mi.src
tag @a[tag=rpg.o.michael_rib_tag1,scores={rpg_mi_dmg=1..}] add rpg.mi.src
execute if entity @a[tag=rpg.mi.src] as @e[tag=rpg.hurt,type=!player,type=!#rpg:no_damage_track] at @s if function rpg:item/extra/michael_by_rib run function rpg:item/extra/michael_rib_hit
tag @a[tag=rpg.mi.src] remove rpg.mi.src
scoreboard players reset * rpg_mi_dmg

# 圣焰的存续：引信、余烬与熄灭
execute as @e[tag=rpg.mi.fuse] at @s run function rpg:item/extra/michael_fuse
execute as @e[tag=rpg.mi.marked] at @s run function rpg:item/extra/michael_ember
scoreboard players set #mi_live rpg_mi_tmp 0
execute if entity @e[tag=rpg.mi.marked,limit=1] run scoreboard players set #mi_live rpg_mi_tmp 1
execute if entity @e[tag=rpg.mi.fuse,limit=1] run scoreboard players set #mi_live rpg_mi_tmp 1
