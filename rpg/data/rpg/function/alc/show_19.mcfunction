execute store result storage rpg:alc d.a0 int 1 run clear @s minecraft:breeze_rod[!minecraft:custom_data] 0
execute store result storage rpg:alc d.a1 int 1 run clear @s minecraft:phantom_membrane[!minecraft:custom_data] 0
execute store result storage rpg:alc d.a2 int 1 run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"soul"}] 0
execute store result storage rpg:alc d.a3 int 1 run clear @s minecraft:paper[minecraft:custom_data~{rpg_mat:"sp_star"}] 0
data modify storage rpg:alc d.z set value 0
function rpg:alc/show_19_m with storage rpg:alc d
