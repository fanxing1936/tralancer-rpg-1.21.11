execute store result storage rpg:alc d.a0 int 1 run clear @s minecraft:bone[!minecraft:custom_data] 0
execute store result storage rpg:alc d.a1 int 1 run clear @s minecraft:glowstone_dust[!minecraft:custom_data] 0
data modify storage rpg:alc d.z set value 0
function rpg:alc/show_5_m with storage rpg:alc d
