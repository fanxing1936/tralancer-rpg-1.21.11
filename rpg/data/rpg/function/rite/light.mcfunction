# 圣水浇上，图腾点燃。烧法取决于旁边站着谁 ——
# 一个魔化到顶的人在场，仪式就不再是净化，而是反转。
tag @s add rpg.totem.lit
scoreboard players set @s rpg_totem 200
playsound minecraft:item.bottle.empty player @a[distance=..16] ~ ~ ~ 1 0.8
execute if entity @a[distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_inv
execute unless entity @a[distance=..7,scores={rpg_taint=100}] run function rpg:rite/light_pure
