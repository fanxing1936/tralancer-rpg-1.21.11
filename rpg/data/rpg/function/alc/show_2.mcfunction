execute store result storage rpg:alc d.a0 int 1 run clear @s minecraft:prismarine_shard[!minecraft:custom_data] 0
execute store result storage rpg:alc d.a1 int 1 run clear @s minecraft:prismarine_crystals[!minecraft:custom_data] 0
data modify storage rpg:alc d.z set value 0
function rpg:alc/show_2_m with storage rpg:alc d
