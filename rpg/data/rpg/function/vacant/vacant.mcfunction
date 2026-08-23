# 空缺者的显形与反扑。两条走查，都带类型。
execute as @e[type=minecraft:villager,tag=rpg.vacant] at @s if entity @a[tag=rpg.h.holy_weapon_tag1,distance=..16] run function rpg:vacant/reveal
execute as @e[type=minecraft:villager,tag=rpg.vacant,tag=rpg.hurt] at @s run function rpg:vacant/lash
