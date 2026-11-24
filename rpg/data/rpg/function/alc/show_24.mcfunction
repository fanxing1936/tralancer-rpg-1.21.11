execute store result storage rpg:alc d.a0 int 1 run clear @s minecraft:ender_pearl[!minecraft:custom_data] 0
execute store result storage rpg:alc d.a1 int 1 run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_star"}] 0
data modify storage rpg:alc d.z set value 0
function rpg:alc/show_24_m with storage rpg:alc d
